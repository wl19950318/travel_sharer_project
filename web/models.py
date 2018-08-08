from __future__ import unicode_literals

from django.db import models

# Create your models here.

class UserInfo(models.Model):
    email = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    pwd = models.CharField(max_length=100)
    code = models.IntegerField()
    verify = models.CharField(max_length=2)

    def __str__(self):
        return self.email