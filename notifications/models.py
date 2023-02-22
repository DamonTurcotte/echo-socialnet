from django.db import models
from django.utils import timezone
import math


class Alerts(models.Model):
    recipient = models.ForeignKey('users.EchoUser', on_delete=models.CASCADE, related_name='notifs')
    by_user = models.ForeignKey('users.EchoUser', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    follow = models.ForeignKey('users.Follow', on_delete=models.CASCADE, blank=True, null=True)
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, blank=True, null=True)

    ALERT_TYPE = (
        ('follow', 'follow'),
        ('reply', 'reply'),
        ('repost', 'repost'),
        ('like', 'like')
    )

    type = models.CharField(max_length=7, choices=ALERT_TYPE)

    def __str__(self):
        if self.type == 'follow':
            return f'{self.by_user.username} followed {self.recipient.username}'
        if self.type == 'like':
            return f'{self.by_user.username} liked {self.post.uuid}'#type:ignore
        if self.type == 'repost':
            return f'{self.by_user.username} reposted {self.post.uuid}'#type:ignore
        if self.type == 'reply':
            return f'{self.by_user.username} replied to {self.post.uuid}'#type:ignore
        
    def when_alert(self):
        now = timezone.now().date()
        when = self.timestamp.date()
        diff = (now - when).days

        if diff == 0:
            return 'today'
        
        elif diff == 1:
            return 'yesterday'
        
        elif diff < 7:
            return f'{diff} days ago'
        
        elif diff < 30:
            weeks = math.floor(diff / 7)
            if weeks == 1:
                return '1 week ago'
            else:
                return f'{weeks} weeks ago'
            
        elif diff < 360:
            months = math.floor(diff / 30)
            if months == 1:
                return '1 month ago'
            else:
                return f'{months} months ago'
            
        else:
            years = math.floor(diff / 360)
            if years == 1:
                return '1 year ago'
            else:
                return f'{years} years ago'
