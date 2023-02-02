from django.db import models
from django.contrib.auth.models import AbstractUser
from echo.utils import time_between
import uuid
from io import BytesIO
from PIL import Image


class EchoUser(AbstractUser):
    app_name = 'users'

    id = models.BigAutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4)
    bio = models.TextField(max_length=150, null=True, blank=True)
    avatar = models.ImageField(default='users/default.png', upload_to='users/', null=True, blank=True)
    follow = models.ManyToManyField('self', through='Follow', blank=True, symmetrical=False)

    class Meta:
        ordering = ['username', 'uuid', 'bio', 'avatar']

    def __str__(self):
        return self.username
    
    def since_last_login(self):
        return time_between(self.last_login)
    
    def num_followers(self):
        return self.followers.count()#type:ignore

    def num_following(self):
        return self.following.count#type:ignore

    
class Follow(models.Model):
    echouser = models.ForeignKey(EchoUser, on_delete=models.CASCADE, related_name='following')
    follow = models.ForeignKey(EchoUser, on_delete=models.CASCADE, related_name='followers')
    followed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.echouser} >> {self.follow} | {self.followed_at}'

    def since_follow(self):
        return time_between(self.followed_at)
