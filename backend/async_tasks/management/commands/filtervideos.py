import time
from collections import defaultdict

from django.core.management.base import BaseCommand
from django.db.models import F
from django.db import transaction

from processes.models import Process, ProcessVideo
from async_tasks.recommendations import get_recommendations


PACK_SIZE = 1  # Pack size for fetching processes



class Command(BaseCommand):
    help = 'Command for filtering videos per process'

    def _fetch_data_from_db(self):
        process_ids = Process.objects.filter(
            status=Process.ProcessStatus.WAITING_FOR_FILTERING_DATA
        ).values(
            'id'
        ).all()[:PACK_SIZE]
        process_ids = [p['id'] for p in process_ids]
        # TODO:::add fetching featured list
        featued_links = []

        data_for_fetching = dict(
            video_title=F('video__title'),
            video_description=F('video__description'),
            video_source=F('video__channel__cs_channel__source__name'),
            video_tag=F('video__tv_videos__tag__name'),
            video_category=F('video__category__name'),

            youtube_positive_mark_number=F('video__youtube_data__positive_mark_number'),
            youtube_negative_mark_number=F('video__youtube_data__negative_mark_number'),
            youtube_view_count=F('video__youtube_data__view_count'),
            youtube_comment_count=F('video__youtube_data__comment_count'),

            search_data=F('process__search_data'),

            process_source=F('process__pc_processes__category__name'),
            process_tag=F('process__ps_processes__source__name'),
            process_category=F('process__pt_processes__tag__name'),

            mark_information_quality=F('video__um_videos__information_quality'),
            mark_medical_practice_quality=F('video__um_videos__medical_practice_quality'),
            mark_description_quality=F('video__um_videos__description_quality'),
            mark_practical_usage_availability=F('video__um_videos__practical_usage_availability'),
            mark_user_id=F('video__um_videos__user__id')
        )
        # TODO:::add fetching with parts via the limit / offset
        # TODO:::use group by
        processes = ProcessVideo.objects.annotate(
            **data_for_fetching
        ).values(
            'process_id', 'video_id', *data_for_fetching.keys()
        ).filter(
            process__id__in=process_ids
        ).all()

        return processes, featued_links

    def _update_data(self, sorted_data: dict) -> None:
        with transaction.atomic():
            for process_id, ordered_videos in sorted_data.items():
                for video_order, video_id in ordered_videos.items():
                    ProcessVideo.objects.filter(
                        process_id=process_id,
                        video_id=video_id
                    ).update(
                        video_order=video_order
                    )

                Process.objects.filter(
                    id=process_id
                ).update(
                    status=Process.ProcessStatus.SUCCESS
                )

    def _handle(self):
        processes, featued_links = self._fetch_data_from_db()

        result_data = get_recommendations(processes, featued_links)

        self._update_data(result_data)

    def handle(self, *args, **options):
        while True:
            self._handle()
            time.sleep(1)
