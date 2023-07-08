from django.contrib import admin
from . import models

admin.site.register(models.EchoUser)
admin.site.register(models.Follow)