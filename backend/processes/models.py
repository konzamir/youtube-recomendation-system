from enum import Enum

from django.db import models
from django.contrib.auth.models import User

from youtube.models import Video


class ProcessStatusEnum(Enum):
    STARTED = ''
    GETTING_BASE_DATA = ''
    GETTING_FULL_DATA = ''
    FILTERING_DATA = ''
    SUCCESS = ''
    INVALID = ''


class Process(models.Model):
    status = models.CharField(
        max_length=5,
        choices=[(item, item.value) for item in ProcessStatusEnum]
    )
    youtube_video_group = models.CharField(max_length=64)

    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE
    )

    updated_at = models.DateTimeField(db_index=True, auto_now=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)


class ProcessVideo(models.Model):
    video = models.ForeignKey(
        to=Video, on_delete=models.CASCADE
    )
    process = models.ForeignKey(
        to=Process, on_delete=models.CASCADE
    )
