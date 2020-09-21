from django.db import models


class Links(models.Model):

    etag = models.CharField(max_length=256)
    published_at = models.DateTimeField(db_index=True)
    channel_id = models.CharField(max_length=64)
    title = models.TextField()
    video_id = models.CharField(max_length=64, db_index=True, unique=True)
    description = models.TextField()
    channel_title = models.CharField(max_length=128)

    preview_url = models.CharField(max_length=512)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)

    updated_at = models.DateTimeField(db_index=True, auto_now=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    
    def __str__(self):
        return f'{self.title}'
