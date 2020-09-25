from django.db import models
from django.contrib.auth.models import User


class YoutubeCredentials(models.Model):
    token = models.CharField(max_length=256, null=True)
    refresh_token = models.CharField(max_length=256, null=True)
    token_uri = models.CharField(max_length=256, null=True)
    client_id = models.CharField(max_length=256, null=True)
    client_secret = models.CharField(max_length=256, null=True)
    expiry = models.DateTimeField(null=True)

    user = models.OneToOneField(
        to=User, on_delete=models.CASCADE
    )
