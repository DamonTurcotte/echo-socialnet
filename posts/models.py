from django.db import models
from users.models import EchoUser

class Posts(models.Model):
    app_name = 'posts'
    
    echouser = models.ForeignKey('users.EchoUser', on_delete=models.CASCADE)
    post = models.TextField(max_length=280)
    timestamp = models.DateTimeField(auto_now_add=True)
    