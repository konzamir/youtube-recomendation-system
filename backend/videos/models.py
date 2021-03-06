from django.db import models
from django.contrib.auth.models import User

from filters.models import Tag, Category, Source


class Channel(models.Model):
    youtube_id = models.CharField(max_length=128)
    name = models.CharField(max_length=256)
    country = models.CharField(max_length=4)
    description = models.TextField()
    keywords = models.TextField()


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

    status = models.IntegerField(
        choices=VideoStatus.choices,
        default=VideoStatus.NOT_CHECKED
    )

    title = models.CharField(max_length=256)
    description = models.TextField()

    channel = models.ForeignKey(
        to=Channel, on_delete=models.CASCADE
    )
    youtube_data = models.OneToOneField(
        to=YoutubeData, on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        to=Category, on_delete=models.CASCADE, null=True
    )

    updated_at = models.DateTimeField(db_index=True, auto_now=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)

    # def __str__(self):
    #     return self.title


# TODO:::move to accounts
class Featured(models.Model):
    class Meta:
        unique_together = ['video', 'user']
    video = models.ForeignKey(
        to=Video, on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE
    )

    updated_at = models.DateTimeField(db_index=True, auto_now=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)

    # def __str__(self):
    #     return f'{self.user.id} -> {self.video.title}'


# TODO:::move to accounts
class UserMark(models.Model):
    class Meta:
        unique_together = ['video', 'user']
    video = models.ForeignKey(
        to=Video, on_delete=models.CASCADE, related_name='um_videos'
    )
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name='um_user'
    )
    information_quality = models.FloatField(default=0, null=True)
    medical_practice_quality = models.FloatField(default=0, null=True)
    description_quality = models.FloatField(default=0, null=True)
    practical_usage_availability = models.FloatField(default=0, null=True)

    # def __str__(self):
    #     return f'{self.user.id} -> {self.video.title}'


class TagVideo(models.Model):
    class Meta:
        unique_together = ['video', 'tag']

    tag = models.ForeignKey(
        to=Tag, on_delete=models.CASCADE, related_name='tv_tags'
    )
    video = models.ForeignKey(
        to=Video, on_delete=models.CASCADE, related_name='tv_videos'
    )


class ChannelSource(models.Model):
    class Meta:
        unique_together = ['source', 'channel']

    source = models.ForeignKey(
        to=Source, on_delete=models.CASCADE, related_name='cs_sources'
    )
    channel = models.ForeignKey(
        to=Channel, on_delete=models.CASCADE, related_name='cs_channel'
    )
