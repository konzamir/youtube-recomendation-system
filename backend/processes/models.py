from django.db import models
from django.contrib.auth.models import User

from videos.models import Video


class Process(models.Model):
    class ProcessStatus(models.IntegerChoices):
        WAITING_FOR_START = 0
        STARTED = 1
        GETTING_BASE_DATA = 2
        GETTING_FULL_DATA = 3
        FILTERING_DATA = 4
        SUCCESS = 5
        INVALID = 6

    status = models.IntegerField(
        choices=ProcessStatus.choices,
        default=ProcessStatus.WAITING_FOR_START
    )
    youtube_video_group = models.CharField(max_length=64, null=True, default=None)
    in_progress = models.BooleanField(default=False)
    search_data = models.TextField(null=False)

    invalid_msg = models.CharField(max_length=128, null=True)

    next_process = models.IntegerField(default=None, null=True)
    prev_process = models.IntegerField(default=None, null=True)

    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE
    )

    updated_at = models.DateTimeField(db_index=True, auto_now=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)

    def __str__(self):
        return f'{self.prev_process} -> {self.id} -> {self.next_process}'


class ProcessVideo(models.Model):
    class Meta:
        unique_together = ['video', 'process']
    video = models.ForeignKey(
        to=Video, on_delete=models.CASCADE
    )
    process = models.ForeignKey(
        to=Process, on_delete=models.CASCADE
    )
