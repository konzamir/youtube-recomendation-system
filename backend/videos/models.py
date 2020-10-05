from django.db import models
from django.contrib.auth.models import User

from filters import models as filters_models


class Channel(models.Model):
    youtube_id = models.CharField(max_length=128)
    name = models.CharField(max_length=64)
    country = models.CharField(max_length=4)
    description = models.TextField()
    keywords = models.TextField()

    source = models.ForeignKey(
        to=filters_models.Source, on_delete=models.CASCADE, null=True
    )


class ImagePreview(models.Model):
    link = models.CharField(max_length=256)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)


class YoutubeData(models.Model):
    etag = models.CharField(max_length=128)
    pub_date = models.DateTimeField()
    video_hash = models.CharField(max_length=64, unique=True)

    positive_mark_number = models.IntegerField(default=0)
    negative_mark_number = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)

    image_preview = models.OneToOneField(
        to=ImagePreview, on_delete=models.CASCADE
    )


class Video(models.Model):
    class VideoStatus(models.IntegerChoices):
        # TODO:::add in progress status
        NOT_CHECKED = 0
        CHECKED = 1
        QUALITATIVE = 2
        NON_QUALITATIVE = 3

    status = models.IntegerField(
        choices=VideoStatus.choices,
        default=VideoStatus.NOT_CHECKED
    )
    practical_usage_availability = models.BooleanField(null=True)
    title = models.CharField(max_length=256)
    description = models.TextField()

    channel = models.ForeignKey(
        to=Channel, on_delete=models.CASCADE
    )
    youtube_data = models.OneToOneField(
        to=YoutubeData, on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        to=filters_models.Category, on_delete=models.CASCADE, null=True
    )

    updated_at = models.DateTimeField(db_index=True, auto_now=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)

    def __str__(self):
        return self.title


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
    information_quality = models.IntegerField(null=True)
    medical_practice_quality = models.IntegerField(null=True)
    description_quality = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.user.id} -> {self.video.title}'


class Tag(models.Model):
    name = models.CharField(max_length=64)
    video_id = models.ForeignKey(
        to=Video, on_delete=models.CASCADE
    )
