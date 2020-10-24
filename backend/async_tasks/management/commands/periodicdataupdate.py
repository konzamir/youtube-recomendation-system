import time
from django.core.management.base import BaseCommand

from videos.models import Video


PACK_SIZE = 500
SLEEP_TIME = 7 * 24 * 60 * 60  # 7 days for periodic update


class Command(BaseCommand):
    help = 'Command for marking videos to update necessary data'

    def _handle(self):
        Video.objects.filter(
            status=Video.VideoStatus.CHECKED
        ).update(
            status=Video.VideoStatus.NOT_CHECKED
        )

    def handle(self, *args, **options):
        while True:
            time.sleep(SLEEP_TIME)
            self._handle()
