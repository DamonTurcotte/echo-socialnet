from django.db import models
from users.models import EchoUser

class Posts(models.Model):
    post = models.TextField(max_length=140)