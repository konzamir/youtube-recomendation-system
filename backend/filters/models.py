from django.db import models
from django.contrib.auth.models import User

from youtube.models import Video


class Source(models.Model):
    name = models.CharField(max_length=64)


class VideoType(models.Model):
    name = models.CharField(max_length=64)


class Destination(models.Model):
    name = models.CharField(max_length=64)


class UserMark(models.Model):
    video = models.ForeignKey(
        to=Video, on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE
    )
    information_quality = models.IntegerField()
    medical_practice_quality = models.IntegerField()
    description_quality = models.IntegerField()

    def __str__(self):
        return f'{self.user.id} -> {self.video.title}'
