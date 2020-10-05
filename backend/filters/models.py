from django.db import models


class Source(models.Model):
    name = models.CharField(max_length=64)


class Category(models.Model):
    name = models.CharField(max_length=64)
    youtube_id = models.CharField(max_length=128)
    etag = models.CharField(max_length=64)
