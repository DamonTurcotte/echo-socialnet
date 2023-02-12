from django.db import models
from django.urls import reverse
from echo.utils import time_between
import uuid
   

class Chat(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    users = models.ManyToManyField('users.EchoUser', auto_created=True, through='PvtMessage', through_fields=('chat', 'sender', 'receiver'))
    last_user = models.CharField(max_length=50, null=True, blank=True)
    last_message = models.CharField(max_length=50, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('message', args=[str(self.uuid)])
    
    def when_last(self):
        return time_between(self.timestamp)


class PvtMessage(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='chat_messages')
    sender = models.ForeignKey('users.EchoUser', on_delete=models.CASCADE, null=True, blank=True, related_name='sent_messages')
    receiver = models.ForeignKey('users.EchoUser', on_delete=models.CASCADE, null=True, blank=True, related_name='received_messages')
    message = models.TextField(max_length=280)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender} >> {self.receiver} @ {self.timestamp}'
    
    def when_last(self):
        return time_between(self.timestamp)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if len(self.message) > 40:
            self.chat.last_message =  self.message[0:36] + '...'
        else:
            self.chat.last_message = self.message[0:39]
        
        self.chat.last_user = self.sender.username#type:ignore
        self.chat.timestamp = self.timestamp
        self.chat.save()
    


