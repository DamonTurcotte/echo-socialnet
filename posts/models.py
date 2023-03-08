from django.db import models
import math
import uuid
from echo.utils import time_between
from django.urls import reverse
from notifications.models import Alerts


class Post(models.Model):
    app_name = 'posts'
    
    uuid = models.UUIDField(default=uuid.uuid4)
    echouser = models.ForeignKey('users.EchoUser', on_delete=models.CASCADE)
    post = models.TextField(max_length=280)
    image = models.ImageField(upload_to="posts/", null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField('users.EchoUser', related_name='liked')
    reply_to = models.ForeignKey('Post', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    repost_of = models.ForeignKey('Post', on_delete=models.CASCADE, null=True, blank=True, related_name='reposts')
    article_comment = models.ForeignKey('news.Articles', on_delete=models.CASCADE, null=True, blank=True, related_name='article_comments')
    article_share = models.ForeignKey('news.Articles', on_delete=models.CASCADE, null=True, blank=True, related_name='article_shares')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.reply_to != None:
            Alerts.objects.create(
                type='reply',
                recipient=self.reply_to.echouser,  # type:ignore
                by_user=self.echouser,
                post=self
            )

        if self.repost_of != None:
            Alerts.objects.create(
                type='repost',
                recipient=self.repost_of.echouser,  # type:ignore
                by_user=self.echouser,
                post=self
            )

    def __str__(self):
        post_return = str(self.post).strip()
        if len(post_return) > 50:
            post_return = f'{post_return[0:48].strip()}...'

        return f'{self.echouser} || {self.timestamp} || {post_return}'
    
    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.uuid)])
    
    def num_replies(self):
        total = self.replies.count()#type:ignore
        if total > 1000000:
            total = f'{math.floor(total / 1000000)}M'
        elif total > 1000:
            total = f'{math.floor(total / 1000)}K'
        elif total == 0:
            total = ''
        return total
    
    def num_reposts(self):
        total = self.reposts.count()# type:ignore
        if total > 1000000:
            total = f'{math.floor(total / 1000000)}M'
        elif total > 1000:
            total = f'{math.floor(total / 1000)}K'
        elif total == 0:
            total = ''
        return total
    
    def num_likes(self):
        total = self.likes.count()
        if total > 1000000:
            total = f'{math.floor(total / 1000000)}M'
        elif total > 1000:
            total = f'{math.floor(total / 1000)}K'
        elif total == 0:
            total = ''
        return total
    
    def when_posted(self):
        return time_between(self.timestamp)
