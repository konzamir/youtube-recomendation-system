import pytz
import time
import logging

import aniso8601
from django.core.management.base import BaseCommand
from django.db import transaction
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from helpers.user_auth_validation import is_user_youtube_auth_valid
from processes.models import Process, ProcessVideo
from videos.models import Video, ImagePreview, Channel, YoutubeData
from accounts.models import YoutubeCredentials
from helpers.custom_encoders import encode_str


PACK_SIZE = 500
VIDEOS_RESULTS = 25
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'This command is fetching the base video data.'

    def _fetch_videos(self, processes):
        try:
            for p in processes:
                credentials = Credentials(
                    token=p.user.youtubecredentials.token,
                    refresh_token=p.user.youtubecredentials.refresh_token,
                    token_uri=p.user.youtubecredentials.token_uri,
                    client_id=p.user.youtubecredentials.client_id,
                    client_secret=p.user.youtubecredentials.client_secret,
                    expiry=p.user.youtubecredentials.expiry.astimezone(pytz.UTC).replace(tzinfo=None)
                )
                credentials = is_user_youtube_auth_valid(credentials)
                if not credentials:
                    YoutubeCredentials.objects.filter(id=p.user.youtubecredentials.id).delete()
                    logger.warning('YouTube credentials were invalid for user with id %s', p.user_id)

                    continue

                youtube = build("youtube", "v3", credentials=credentials)
                videos_data = youtube.search().list(
                    part='snippet',
                    type='video',
                    q=p.search_data,
                    maxResults=VIDEOS_RESULTS,
                    pageToken=p.youtube_video_group
                ).execute()

                for video in videos_data['items']:
                    snippet = video['snippet']

                    image, _ = ImagePreview.objects.get_or_create(
                        link=snippet['thumbnails']['high']['url'],
                        width=snippet['thumbnails']['high']['width'],
                        height=snippet['thumbnails']['high']['height']
                    )
                    channel, _ = Channel.objects.get_or_create(
                        youtube_id=snippet['channelId'],
                        name=snippet['channelTitle']
                    )
                    youtube_data, _ = YoutubeData.objects.get_or_create(
                        etag=video['etag'],
                        video_hash=video['id']['videoId'],
                        defaults={
                            'pub_date': aniso8601.parse_datetime(snippet['publishedAt']),
                            'image_preview': image,
                        }
                    )
                    db_video, _ = Video.objects.get_or_create(
                        title=encode_str(snippet['title']),
                        description=encode_str(snippet['description']),
                        channel=channel,
                        youtube_data=youtube_data
                    )
                    ProcessVideo.objects.get_or_create(
                        video_id=db_video.id,
                        process_id=p.id
                    )

                if videos_data.get('nextPageToken'):
                    new_process, _ = Process.objects.get_or_create(
                        youtube_video_group=videos_data['nextPageToken'],
                        search_data=p.search_data,
                        user_id=p.user_id,
                        prev_process=p.id
                    )
                    # TODO:::add creating filters per process
                    Process.objects.filter(id=p.id).update(
                        next_process=new_process.id,
                    )

                Process.objects.filter(id=p.id).update(
                    status=Process.ProcessStatus.WAITING_FOR_FETCHING_FULL_DATA
                )

            transaction.commit()
        except Exception as exc:
            logger.error(exc, exc_info=True)
            transaction.rollback()

    def handle(self, *args, **options):
        transaction.set_autocommit(False)

        while True:
            # TODO:::optimize with single DB request
            processes = Process.objects.prefetch_related(
                'user__youtubecredentials'
            ).filter(
                status=Process.ProcessStatus.WAITING_FOR_FETCHING_BASE_DATA,
                active=True,
            ).all()[:PACK_SIZE]

            if processes:
                # TODO::implement in future
                # self._mark_processes_in_progress(...)
                self._fetch_videos(processes)

            time.sleep(1)
