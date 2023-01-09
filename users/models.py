from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
import uuid


class EchoUser(AbstractUser):
    app_name = 'users'

    id = models.BigAutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4)
    bio = models.TextField(max_length=150, null=True, blank=True)
    avatar = models.ImageField(default='users/default.png', upload_to='users/', null=True, blank=True)

    class Meta:
        ordering = ['username', 'uuid', 'bio', 'avatar']

    def __str__(self):
        return self.username