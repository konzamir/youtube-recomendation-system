from collections import defaultdict
from helpers.custom_encoders import decode_str


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


def get_recommendations(unformated_process_data, featued_links):
    formated_data = _format_data(unformated_process_data)
    filtered_data = _filter_data(formated_data)
    sorted_data = _sort_data(filtered_data, featued_links)

    return sorted_data


def _format_data(processes):
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
            "negative_mark_number": -1 * process_data['youtube_negative_mark_number'],
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


def _compare_criteria_lists(process_criteria: set, video_criteria: set) -> bool:
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


def _filter_data(formated_data: BASE_DATA_STRUCTURE) -> dict:
    """
    Criteria are:
        * sources
        * tags
        * categories
    """
    videos_for_filtering = defaultdict(set)

    for process_id, process_data in formated_data.items():
        for video_id, video_data in process_data['videos'].items():
            if not _compare_criteria_lists(process_data['sources'], video_data['sources']) and \
                    not _compare_criteria_lists(process_data['tags'], video_data['tags']) and \
                    not _compare_criteria_lists(process_data['categories'], video_data['categories']):
                videos_for_filtering[process_id].add(video_id)
                continue

    for process_id, video_ids in videos_for_filtering.items():
        for video_id in video_ids:
            del formated_data[process_id]['videos'][video_id]

    return formated_data


def _sort_data(filtered_data: BASE_DATA_STRUCTURE, featured_links: list) -> dict:
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
                    list(v_data['youtube_marks'].values())
                ) + (1 if v_data['description'] else 0) + int(v_id in featured_links)
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
