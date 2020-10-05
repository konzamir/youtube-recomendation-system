import pytz
import time
import logging
from typing import List

import aniso8601
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models.sql.query import F
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build, Resource
from django.contrib.auth.models import User
from helpers.user_auth_validation import is_user_youtube_auth_valid
from processes.models import Process, ProcessVideo
from videos.models import Video, ImagePreview, Channel, YoutubeData
from accounts.models import YoutubeCredentials


PACK_SIZE = 500
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'This command is fetching full video, channel, filters data'

    def _fetch_credentials(self, data: dict) -> Credentials:
        credentials = Credentials(
            token=data['youtube_token'],
            refresh_token=data['youtube_refresh_token'],
            token_uri=data['youtube_token_uri'],
            client_id=data['youtube_client_id'],
            client_secret=data['youtube_client_secret'],
            expiry=data['youtube_client_expiry'].astimezone(pytz.UTC).replace(tzinfo=None)
        )
        credentials = is_user_youtube_auth_valid(credentials)

        return credentials

    def _fetch_video_data(self) -> List[dict]:
        # TODO:::add groupby process_id

        videos = ProcessVideo.objects.select_related(
            'process', 'video',
            'video__youtube_data', 'video__channel'
        ).prefetch_related(
            'user__youtubecredentials'
        ).values(
            'video_id',
            user_id=F('process__user__id'),
            video_hash=F('video__youtube_data__video_hash'),
            video_data_id=F('video__youtube_data__id'),

            channel_id=F('video__channel__id'),
            channel_hash=F('video__channel__youtube_id'),

            youtube_id=F('process__user__youtubecredentials__id'),
            youtube_token=F('process__user__youtubecredentials__token'),
            youtube_refresh_token=F('process__user__youtubecredentials__refresh_token'),
            youtube_token_uri=F('process__user__youtubecredentials__token_uri'),
            youtube_client_id=F('process__user__youtubecredentials__client_id'),
            youtube_client_secret=F('process__user__youtubecredentials__client_secret'),
            youtube_client_expiry=F('process__user__youtubecredentials__expiry'),
        ).filter(
            video__status=Video.VideoStatus.NOT_CHECKED
        ).all()[0:1]#PACK_SIZE]

        return videos

    def _fetch_all_youtube_data(self, youtube_build: Resource, data: dict) -> dict:
        video_data = youtube_build.videos().list(
            part='snippet', id=data['video_hash']
        ).execute()

        video_data = video_data['items'][0]

        tags = video_data['snippet'].get('tags', [])
        category = video_data['snippet']['categoryId']

        print(category)

        return {
            'tags': tags,
            'category': {
                'category_id': category
            }
        }

    def handle(self, *args, **options):
        transaction.set_autocommit(False)

        videos = self._fetch_video_data()

        for video in videos:
            credentials = self._fetch_credentials(video)
            if not credentials:
                YoutubeCredentials.objects.filter(id=video['youtube_id']).delete()
                logger.warning('YouTube credentials were invalid for user with id %s', video['user_id'])

                continue

            youtube_build = build("youtube", "v3", credentials=credentials)
            youtube_fetching_result = self._fetch_all_youtube_data(youtube_build, video)

            print('---')
            print(youtube_fetching_result)
            print('---')

        transaction.commit()
