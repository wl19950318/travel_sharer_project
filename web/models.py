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

class Note(models.Model):
    userId = models.ForeignKey(UserInfo)
    createTime = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    content = models.CharField(max_length=2000)
    picUrl = models.CharField(max_length=500)
    remark = models.CharField(max_length=500)
    #1 Eat 2 Travel 3 Relax
    type = models.CharField(max_length=2)
    views = models.IntegerField()
    likes = models.IntegerField()

    def __str__(self):
        return self.title

class NoteComment(models.Model):
    userId = models.ForeignKey(UserInfo)
    noteId = models.ForeignKey(Note)
    comment = models.CharField(max_length=500)
    createTime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment

class TBicture(models.Model):
    address = models.CharField(max_length=100)
    userId = models.ForeignKey(UserInfo)
    #1 Musician 2 Food lover 3 Photographer 4 Sports
    type = models.CharField(max_length=2)
    #1 Food 2 Destination  3 Hotel 4 Summer
    discover_type = models.CharField(max_length=2)
    title = models.CharField(max_length=100)
    remark = models.CharField(max_length=500)
    picUrl = models.CharField(max_length=500)
    createTime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.address


class NoteCollection(models.Model):
    userId = models.ForeignKey(UserInfo)
    noteId = models.ForeignKey(Note)
    createTime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.createTime




