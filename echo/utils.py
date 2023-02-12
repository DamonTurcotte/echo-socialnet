from django.utils import timezone
import math


def time_between(date):
    now = timezone.now()
    diff = now - date

    if diff.seconds < 60:
         seconds = diff.seconds
         if seconds < 1:
             return 'now'
         elif seconds == 1:
             return '1 second ago'
         else:
             return f'{seconds} seconds ago'

    elif diff.seconds < 3600:
        minutes = math.floor(diff.seconds / 60)
        if minutes == 1:
            return '1 minute ago'
        else:
            return f'{minutes} minutes ago'
        
    elif diff.days < 1:
        hours = math.floor(diff.seconds / 3600)
        if hours == 1:
            return '1 hour ago'
        else:
            return f'{hours} hours ago'
        
    elif diff.days < 7:
        days = diff.days
        if days == 1:
            return '1 day ago'
        else:
            return f'{days} days ago'
        
    elif diff.days < 30:
        weeks = math.floor(diff.days / 7)
        if weeks == 1:
            return '1 week ago'
        else:
            return f'{weeks} weeks ago'
        
    elif diff.days < 365:
        months = math.floor(diff.days / 30)
        if months == 1:
            return '1 month ago'
        else:
            return f'{months} months ago'
        
    else:
        years = math.floor(diff.days / 365)
        if years == 1:
            return '1 year ago'
        else:
            return f'{years} years ago'
        

def make_post_objects(posts_queryset, request_username):
    post_list = list()

    for post in posts_queryset:
        post_view = dict()
        post_view['echouser'] = post.echouser.username
        post_view['echouser_id'] = post.echouser.uuid
        post_view['avatar'] = post.echouser.avatar.url
        post_view['post_id'] = post.uuid
        post_view['post'] = post.post
        post_view['when_posted'] = post.when_posted()
        post_view['num_likes'] = post.num_likes()
        post_view['num_replies'] = post.num_replies()
        post_view['num_reposts'] = post.num_reposts()
        post_view['object'] = ['post']

        alt_post_fields = [
            'reply_to_id',
            'reply_to_name',
            'repost_id',
            'repost_avatar',
            'repost_user',
            'repost_time',
            'repost_post'
        ]

        for field in alt_post_fields:
             post_view[field] = ''

        try:
            post_view['reply_to_id'] = post.reply_to.uuid  # type:ignore
            # type:ignore
            post_view['reply_to_name'] = post.reply_to.echouser.username
            post_view['object'] = 'reply'
        except:
            pass

        try:
            post_view['repost_id'] = post.repost_of.uuid  # type:ignore
            # type:ignore
            post_view['repost_avatar'] = post.repost_of.echouser.avatar.url
            # type:ignore
            post_view['repost_user'] = post.repost_of.echouser.username
            # type:ignore
            post_view['repost_time'] = post.repost_of.when_posted()
            post_view['repost_post'] = post.repost_of.post  # type:ignore
            post_view['object'] = 'repost'
        except:
            pass

        if post.likes.filter(username=request_username).exists():
            post_view['liked'] = ' active'

        else:
            post_view['liked'] = ''

        post_list.append(post_view)

    return post_list
