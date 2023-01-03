from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
import uuid


class CustomUser(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4)
    bio = models.TextField(max_length=150, null=True, blank=True)
    avatar = models.ImageField(default='static/users/default.png', upload_to='static/users/', null=True, blank=True)

    class Meta:
        ordering = []

    def __str__(self):
        return self.username