from django.db import models
from django.contrib.auth.models import User

from filters import models as filters_models


class Channel(models.Model):
    name = models.CharField(max_length=64)
    source = models.ForeignKey(
        to=filters_models.Source, on_delete=models.CASCADE
    )


class ImagePreview(models.Model):
    link = models.CharField(max_length=256)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)


class YoutubeData(models.Model):
    etag = models.CharField(max_length=128)
    pub_date = models.DateTimeField()
    video_hash = models.CharField(max_length=64)
    positive_mark_number = models.IntegerField(default=0)
    negative_mark_number = models.IntegerField(default=0)
    image_preview = models.ForeignKey(
        to=ImagePreview, on_delete=models.CASCADE
    )


class Video(models.Model):
    class VideoStatus(models.IntegerChoices):
        NOT_CHECKED = 0
        QUALITATIVE = 1
        NON_QUALITATIVE = 2

    status = models.IntegerField(
        choices=VideoStatus.choices,
        default=VideoStatus.NOT_CHECKED.value
    )
    practical_usage_availability = models.BooleanField()
    title = models.CharField(max_length=256)
    description = models.TextField()

    video_type = models.ForeignKey(
        to=filters_models.VideoType, on_delete=models.CASCADE
    )
    channel = models.ForeignKey(
        to=Channel, on_delete=models.CASCADE
    )
    youtube_data = models.ForeignKey(
        to=YoutubeData, on_delete=models.CASCADE
    )
    destination = models.ForeignKey(
        to=filters_models.Destination, on_delete=models.CASCADE
    )

    updated_at = models.DateTimeField(db_index=True, auto_now=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)


class Featured(models.Model):
    video = models.ForeignKey(
        to=Video, on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE
    )

    updated_at = models.DateTimeField(db_index=True, auto_now=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)

    def __str__(self):
        return f'{self.user.id} -> {self.video.title}'


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