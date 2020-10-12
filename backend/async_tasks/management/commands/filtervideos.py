from copy import deepcopy
from collections import defaultdict

from django.core.management.base import BaseCommand
from django.db.models import F

from processes.models import Process, ProcessVideo
from helpers.custom_encoders import decode_str


PACK_SIZE = 1  # Pack size for fetching processes
BASE_DATA_STRUCTURE = {
    'videos': defaultdict(lambda: {
        'practical_usage_availability': bool(),
        'title': str(),
        'description': str(),

        'sources': set(),
        'tags': set(),
        'categories': set(),

        'marks': {
            'information_quality': float(),
            'medical_practice_quality': float(),
            'description_quality': float(),
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

        data_for_fetching = dict(
            video_practical_usage_availability=F('video__practical_usage_availability'),
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

        return processes

    def _format_data(self, processes):
        process_video_grouped = defaultdict(lambda: BASE_DATA_STRUCTURE)
        information_quality_set = defaultdict(set)
        medical_practice_quality_set = defaultdict(set)
        description_quality_set = defaultdict(set)

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

            process_video_grouped[process_id]['videos'][video_id]['practical_usage_availability'] = \
                process_data['video_practical_usage_availability']
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

        return process_video_grouped

    def __compare_criteria_lists(self, process_criteria: list, video_criteria: list) -> bool:
        """ Dummy search through the two lists.
        TODO:::in the future update with more quick algorithm
        """
        for pc in process_criteria:
            if pc is None:
                continue

            pc = pc.lower()
            for vc in video_criteria:
                if vc is None:
                    continue

                vc = vc.lower()
                if pc.find(vc) >= 0 or vc.find(pc) >= 0:
                    print('  +++  ', pc, vc)
                    return True

        return False

    def _filter_data(self, formated_data: BASE_DATA_STRUCTURE) -> dict:
        """
        Criteria are:
          * sources
          * tags
          * categories
          * medical practical usage
        """
        videos_for_filtering = defaultdict(set)

        for process_id, process_data in formated_data.items():
            for video_id, video_data in process_data['videos'].items():
                if video_data['practical_usage_availability'] is False or \
                        not self.__compare_criteria_lists(process_data['sources'], video_data['sources']) and \
                        not self.__compare_criteria_lists(process_data['tags'], video_data['tags']) and \
                        not self.__compare_criteria_lists(process_data['categories'], video_data['categories']):
                    videos_for_filtering[process_id].add(video_id)
                    continue

        for process_id, video_ids in videos_for_filtering.items():
            for video_id in video_ids:
                del formated_data[process_id]['videos'][video_id]

        return formated_data

    def _sort_data(self, filtered_data: BASE_DATA_STRUCTURE) -> dict:
        """
        Criteria are:
          * user marks
          * youtube marks
        """
        sorted_data = {}

        print(filtered_data)

        return sorted_data

    def _update_data(self, sorted_data):
        pass

    def handle(self, *args, **options):
        processes = self._fetch_data_from_db()

        formated_data = self._format_data(processes)
        filtered_data = self._filter_data(formated_data)
        sorted_data = self._sort_data(filtered_data)

        self._update_data(sorted_data)
