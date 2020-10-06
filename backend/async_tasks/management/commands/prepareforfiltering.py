import logging
import time

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import F, Sum, Count

from processes.models import Process
from videos.models import Video


PACK_SIZE = 500
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Command for updating process status, when all videos will be checked'

    def handle(self, *args, **options):
        transaction.set_autocommit(False)

        while True:
            try:
                self._handle()
                time.sleep(1)
            except Exception as exc:
                logger.error(exc, exc_info=True)
                transaction.rollback()

    def _handle(self):
        """ For checked the Sum is using, because it is a enum field, values
        can be only 1 or 0, so we need to get sum, to check, how many videos are
        already CHECKED.
        """

        # TODO:::replace usage with Process
        processes = Video.objects.prefetch_related(
            'pv_videos__process'
        ).values(
            process_id=F('pv_videos__process__id')
        ).filter(
            pv_videos__process__id__in=Process.objects.filter(
                status=Process.ProcessStatus.WAITING_FOR_FETCHING_FULL_DATA
            )
        ).annotate(
            checked=Sum('status'), total=Count('status')
        ).all()[:PACK_SIZE]

        for process in processes:
            if process['checked'] == process['total']:
                Process.objects.filter(
                    id=process['process_id']
                ).update(
                    status=Process.ProcessStatus.WAITING_FOR_FILTERING_DATA
                )

        transaction.commit()
