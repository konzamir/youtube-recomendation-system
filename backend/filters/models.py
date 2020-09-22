from django.db import models


class Source(models.Model):
    name = models.CharField(max_length=64)


class VideoType(models.Model):
    name = models.CharField(max_length=64)


class Destination(models.Model):
    name = models.CharField(max_length=64)
