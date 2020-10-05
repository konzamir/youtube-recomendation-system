from django.db import models
from django.contrib.auth.models import User

from videos.models import Video


class Process(models.Model):
    class ProcessStatus(models.IntegerChoices):
        # TODO:::add current states for each part of processing
        WAITING_FOR_FETCHING_BASE_DATA = 0
        WAITING_FOR_FETCHING_FULL_DATA = 1
        WAITING_FOR_FILTERING_DATA = 2
        SUCCESS = 3
        INVALID = 4

    status = models.IntegerField(
        choices=ProcessStatus.choices,
        default=ProcessStatus.WAITING_FOR_FETCHING_BASE_DATA
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
