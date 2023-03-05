from django.db import models
import uuid

app_name = 'news'

class Articles(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    source = models.CharField(max_length=100)
    title = models.CharField(max_length=300)
    description = models.CharField(max_length=300, blank=True, null=True)
    content = models.CharField(max_length=300, blank=True, null=True)
    url = models.URLField()
    image = models.URLField()
    date = models.DateField()
    category = models.CharField(max_length=20, default='general')
    when_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.title[:120]}...'
    
class LastNewsUpdate(models.Model):
    time = models.DateTimeField()