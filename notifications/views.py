from django.shortcuts import render
from notifications.models import Alerts
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta


@login_required
def alerts_view(request):
    delta = timedelta(days=7)
    last_week = timezone.now().date() - delta
    
    if Alerts.objects.filter(recipient=request.user, is_read=False).exclude(by_user=request.user).exists():
        alerts = Alerts.objects.filter(recipient=request.user, is_read=False).exclude(by_user=request.user).order_by('timestamp').reverse()
        follows = alerts.filter(type='follow')
        post_alerts = alerts.exclude(type='follow')
    
    else:
        alerts = Alerts.objects.filter(recipient=request.user, is_read=True, timestamp__gt=last_week).exclude(by_user=request.user).order_by('timestamp').reverse()
        follows = alerts.filter(type='follow')
        post_alerts = alerts.exclude(type='follow')

    notifications = {}

    for alert in alerts:

        notifications[alert.when_alert()] = {
            'follows': {
                'users': [],
                'count': 0,
            },
            'posts': {},
        }

    for follow in follows:
        notifications[alert.when_alert()]['follows']['count'] += 1#type:ignore
        notifications[alert.when_alert()]['follows']['users'].append(follow.by_user)#type:ignore

    for alert in post_alerts:
        if alert.type == 'like':
            uuid = alert.post.uuid#type:ignore
        if alert.type == 'reply':
            uuid = alert.post.reply_to.uuid#type:ignore
        if alert.type == 'repost':
            uuid = alert.post.repost_of.uuid#type:ignore

        try:
            if notifications[alert.when_alert()]['posts'][uuid]:#type:ignore
                pass
        except:
            notifications[alert.when_alert()]['posts'][uuid] = {#type:ignore
                'likes': {
                    'users': [],
                    'post': alert.post,
                    'count': 0,
                },
                'reposts': [],
                'replies': []
            }

        post = notifications[alert.when_alert()]['posts'][uuid]  # type:ignore

        if alert.type == 'like':
            post['likes']['users'].append(alert.by_user)
            post['likes']['count'] += 1

        if alert.type == 'repost':
            instance = {}
            instance['by_user'] = alert.by_user
            instance['repost'] = alert.post
            instance['post'] = alert.post.repost_of#type:ignore
            post['reposts'].append(instance)

        if alert.type == 'reply':
            instance = {}
            instance['by_user'] = alert.by_user
            instance['reply'] = alert.post
            instance['post'] = alert.post.reply_to#type:ignore
            post['replies'].append(instance)

    context = {
        'title': 'Alerts | Echo',
        'alert_dates': notifications
    }

    for alert in alerts:
        alert.is_read = True
        alert.save()

    return render(request, 'notifications/alerts.html', context=context)
