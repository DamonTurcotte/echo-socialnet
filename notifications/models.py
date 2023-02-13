from django.db import models


class Alerts(models.Model):
    recipient = models.ForeignKey('users.EchoUser', on_delete=models.CASCADE, related_name='notifs')
    by_user = models.ForeignKey('users.EchoUser', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    follow = models.ForeignKey('users.Follow', on_delete=models.CASCADE, blank=True, null=True)
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, blank=True, null=True)

    ALERT_TYPE = (
        ('follow', 'follow'),
        ('reply', 'reply'),
        ('repost', 'repost'),
        ('like', 'like')
    )

    type = models.CharField(max_length=7, choices=ALERT_TYPE)