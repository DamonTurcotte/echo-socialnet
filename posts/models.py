from django.db import models
from django.utils import timezone
import math
import uuid


class Post(models.Model):
    app_name = 'posts'
    
    uuid = models.UUIDField(default=uuid.uuid4)
    echouser = models.ForeignKey('users.EchoUser', on_delete=models.CASCADE)
    post = models.TextField(max_length=280)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField('users.EchoUser', related_name='liked')
    reply_to = models.ForeignKey('Post', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['echouser', 'post'], name='unique_like')
        ]

    def __str__(self):
        post_return = str(self.post).strip()
        if len(post_return) > 50:
            post_return = f'{post_return[0:48].strip()}...'

        return f'{self.echouser} || {self.timestamp} || {post_return}'

    def num_likes(self):
        return self.likes.count()

    def when_posted(self):
        now = timezone.now()
        diff = now - self.timestamp

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
