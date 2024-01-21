import datetime

from django.db import models

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    publish_date = models.DateField(auto_now=datetime.datetime.now())
    author = models.CharField(max_length=100)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    author = models.CharField(max_length=100)

