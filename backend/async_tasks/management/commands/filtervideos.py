from collections import defaultdict

from django.core.management.base import BaseCommand
from django.db.models import F, Prefetch

from processes.models import Process
from videos.models import Video

PACK_SIZE = 500


class Command(BaseCommand):
    help = 'Command for filtering videos per process'

    def handle(self, *args, **options):
        # Note, that each process should always contain 25 videos
        # to change it, also update VIDEOS_RESULTS in the `filtervideos.VIDEOS_RESULTS`
        processes = Process.objects.prefetch_related(
            'pv_processes__video'
        ).values(
            process_id=F('id'),

            video_id=F('pv_processes__video__id'),

        ).filter(
            status=Process.ProcessStatus.WAITING_FOR_FILTERING_DATA
        ).all()[:PACK_SIZE]

        process_video_grouped = defaultdict(list)

        for process_data in processes:
            process_id = process_data['process_id']
            del process_data['process_id']
            process_video_grouped[process_id].append(process_data)


            # print(process.processes)
            # print('+++', process.video)
            # print(dir(process))
