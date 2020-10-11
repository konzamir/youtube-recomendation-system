from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=128, unique=True)


class Source(models.Model):
    name = models.CharField(max_length=128, unique=True)


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    youtube_id = models.CharField(max_length=128)
    etag = models.CharField(max_length=64)