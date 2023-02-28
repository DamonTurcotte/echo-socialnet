from django.db import models


class Articles(models.Model):
    source = models.CharField(max_length=100)
    title = models.CharField(max_length=300)
    description = models.CharField(max_length=300, blank=True, null=True)
    url = models.URLField()
    image = models.URLField()
    date = models.DateField()
    category = models.CharField(max_length=20, default='general')
    when_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.title[:30]}... | {self.date}'
    
class LastNewsUpdate(models.Model):
    time = models.DateTimeField()