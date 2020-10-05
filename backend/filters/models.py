from django.db import models


class Source(models.Model):
    name = models.CharField(max_length=64)


class Tag(models.Model):
    name = models.CharField(max_length=64)


class Category(models.Model):
    name = models.CharField(max_length=64)
