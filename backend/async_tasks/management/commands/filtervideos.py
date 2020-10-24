import time
from collections import defaultdict

from django.core.management.base import BaseCommand
from django.db.models import F
from django.db import transaction

from processes.models import Process, ProcessVideo
from helpers.custom_encoders import decode_str


PACK_SIZE = 1  # Pack size for fetching processes
# TODO:::move to class-based objects
BASE_DATA_STRUCTURE = {
    'videos': defaultdict(lambda: {
        'title': str(),
        'description': str(),

        'sources': set(),
        'tags': set(),
        'categories': set(),

        'marks': {
            'information_quality': float(),
            'medical_practice_quality': float(),
            'description_quality': float(),
            'practical_usage_availability': float()
        },

        "youtube_marks": {
            "positive_mark_number": int(),
            "negative_mark_number": int(),
            "view_count": int(),
            "comment_count": int(),
        }
    }),

    'sources': set(),
    'tags': set(),
    'categories': set(),
    "search_data": str()
}


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
        processes = ProcessVideo.objects.annotate(
            **data_for_fetching
        ).values(
            'process_id', 'video_id', *data_for_fetching.keys()
        ).filter(
            process__id__in=process_ids
        ).all()

        return processes, featued_links

    def _format_data(self, processes):
        process_video_grouped = defaultdict(lambda: BASE_DATA_STRUCTURE)

        information_quality_set = defaultdict(set)
        medical_practice_quality_set = defaultdict(set)
        description_quality_set = defaultdict(set)
        practical_usage_availability_set = defaultdict(set)

        for process_data in processes:
            process_id = process_data['process_id']
            process_video_grouped[process_id]["search_data"] = process_data['search_data']

            process_video_grouped[process_id]['sources'].add(
                decode_str(process_data['process_source']))
            process_video_grouped[process_id]['tags'].add(
                decode_str(process_data['process_tag']))
            process_video_grouped[process_id]['categories'].add(
                decode_str(process_data['process_category']))

            video_id = process_data['video_id']

            process_video_grouped[process_id]['videos'][video_id]['title'] = \
                decode_str(process_data['video_title'])
            process_video_grouped[process_id]['videos'][video_id]['description'] = \
                decode_str(process_data['video_description'])
            process_video_grouped[process_id]['videos'][video_id]['sources'].add(
                decode_str(process_data['video_source']))
            process_video_grouped[process_id]['videos'][video_id]['tags'].add(
                decode_str(process_data['video_tag']))
            process_video_grouped[process_id]['videos'][video_id]['categories'].add(
                decode_str(process_data['video_category']))

            process_video_grouped[process_id]['videos'][video_id]['youtube_marks'] = {
                "positive_mark_number": process_data['youtube_positive_mark_number'],
                "negative_mark_number": process_data['youtube_negative_mark_number'],
                "view_count": process_data['youtube_view_count'],
                "comment_count": process_data['youtube_comment_count']
            }

            if process_data['mark_information_quality'] is not None and \
                    process_data['mark_information_quality'] > 0 and \
                    process_data['mark_user_id'] not in information_quality_set[video_id]:

                process_video_grouped[process_id]['videos'][video_id]['marks']['information_quality'] = \
                    (process_video_grouped[process_id]['videos'][video_id]['marks']['information_quality'] *
                     len(information_quality_set[video_id]) + process_data['mark_information_quality']
                    ) / float(len(information_quality_set[video_id]) + 1)
                information_quality_set[video_id].add(process_data['mark_user_id'])

            if process_data['mark_medical_practice_quality'] is not None and \
                    process_data['mark_medical_practice_quality'] and \
                    process_data['mark_user_id'] not in medical_practice_quality_set[video_id]:

                process_video_grouped[process_id]['videos'][video_id]['marks']['medical_practice_quality'] = \
                    (process_video_grouped[process_id]['videos'][video_id]['marks']['medical_practice_quality'] *
                     len(medical_practice_quality_set[video_id]) + process_data['mark_medical_practice_quality']
                    ) / float(len(medical_practice_quality_set[video_id]) + 1)
                medical_practice_quality_set[video_id].add(process_data['mark_user_id'])

            if process_data['mark_description_quality'] is not None and \
                    process_data['mark_description_quality'] > 0 and \
                    process_data['mark_user_id'] not in description_quality_set:

                process_video_grouped[process_id]['videos'][video_id]['marks']['description_quality'] = \
                    (process_video_grouped[process_id]['videos'][video_id]['marks']['description_quality'] *
                     len(description_quality_set[video_id]) + process_data['mark_description_quality']
                    ) / float(len(description_quality_set[video_id]) + 1)
                description_quality_set[video_id].add(process_data['mark_user_id'])

            if process_data['mark_practical_usage_availability'] is not None and \
                    process_data['mark_practical_usage_availability'] > 0 and \
                    process_data['mark_user_id'] not in practical_usage_availability_set:

                process_video_grouped[process_id]['videos'][video_id]['marks']['practical_usage_availability'] = \
                    (process_video_grouped[process_id]['videos'][video_id]['marks']['practical_usage_availability'] *
                     len(practical_usage_availability_set[video_id]) + process_data['practical_usage_availability']
                    ) / float(len(practical_usage_availability_set[video_id]) + 1)
                practical_usage_availability_set[video_id].add(process_data['mark_user_id'])

        return process_video_grouped

    def __compare_criteria_lists(self, process_criteria: set, video_criteria: set) -> bool:
        """ Dummy search through the two lists because total number of elements
        will not be bigger then 100.
        """
        process_criteria = list(process_criteria)
        video_criteria = list(video_criteria)

        if process_criteria[0] is None or video_criteria[0] is None:
            # For cases when no criteria were chosen
            return True

        for pc in process_criteria:
            if pc is None:
                continue

            pc = pc.lower()
            for vc in video_criteria:
                if vc is None:
                    continue

                vc = vc.lower()
                if pc.find(vc) >= 0 or vc.find(pc) >= 0:
                    return True

        return False

    def _filter_data(self, formated_data: BASE_DATA_STRUCTURE) -> dict:
        """
        Criteria are:
          * sources
          * tags
          * categories
        """
        videos_for_filtering = defaultdict(set)

        for process_id, process_data in formated_data.items():
            for video_id, video_data in process_data['videos'].items():
                if not self.__compare_criteria_lists(process_data['sources'], video_data['sources']) and \
                        not self.__compare_criteria_lists(process_data['tags'], video_data['tags']) and \
                        not self.__compare_criteria_lists(process_data['categories'], video_data['categories']):
                    videos_for_filtering[process_id].add(video_id)
                    continue

        for process_id, video_ids in videos_for_filtering.items():
            for video_id in video_ids:
                del formated_data[process_id]['videos'][video_id]

        return formated_data

    def _sort_data(self, filtered_data: BASE_DATA_STRUCTURE, featured_links: list) -> dict:
        """
        Criteria are:
          * description availability
          * is in featured
          * user marks
            * information quality
            * medical practic quality
            * description quality
            * practical usage availability
          * youtube marks
            * positve marks count
            * negative marks count
            * number of views
            * number of comments
        """
        process_video_order = defaultdict(dict)

        for process_id, process_data in filtered_data.items():
            videos = [
                {
                    'video_id': v_id,
                    'marks_sum': sum(
                        list(v_data['marks'].values()) + 
                        list(v_data['youtube_marks'].values()) + 
                        (1 if v_data['description'] else 0) +
                        int(v_id in featured_links)
                    )
                } for v_id, v_data in process_data['videos'].items()
            ]
            videos = sorted(
                videos,
                key=lambda video: video['marks_sum'],
                reverse=True
            )

            process_video_order[process_id] = {
                (index + 1): video['video_id'] for index, video in enumerate(videos)
            }

        return process_video_order

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

        formated_data = self._format_data(processes)
        filtered_data = self._filter_data(formated_data)
        sorted_data = self._sort_data(filtered_data, featued_links)

        self._update_data(sorted_data)

    def handle(self, *args, **options):
        while True:
            self._handle()
            time.sleep(1)
