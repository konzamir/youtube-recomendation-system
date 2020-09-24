from django.db import models
from django.contrib.auth.models import User


class YoutubeCredentials(models.Model):
    token = models.CharField(max_length=256)
    refresh_token = models.CharField(max_length=256)
    token_uri = models.CharField(max_length=256)
    client_id = models.CharField(max_length=256)
    client_secret = models.CharField(max_length=256)
    scopes = models.TextField()

    def get_converted_scopes(self):
        return self.scopes.split(',')

    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE
    )
