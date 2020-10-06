import logging
import time
from typing import List

import pytz
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models.sql.query import F
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build, Resource

from accounts.models import YoutubeCredentials
from helpers.user_auth_validation import is_user_youtube_auth_valid
from processes.models import ProcessVideo
from videos.models import Source, Category, Video, Channel,\
    YoutubeData, Tag, TagVideo, ChannelSource

PACK_SIZE = 10
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
        videos = ProcessVideo.objects.select_related(
            'process', 'video',
            'video__youtube_data', 'video__channel'
        ).prefetch_related(
            'user__youtubecredentials'
        ).values(
            'video_id',
            user_id=F('process__user__id'),
            video_hash=F('video__youtube_data__video_hash'),

            youtube_data_id=F('video__youtube_data__id'),

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
        ).all()[0:PACK_SIZE]

        return videos

    def _make_video_status_in_progress(self, video_ids: list) -> None:
        pass

    def _fetch_all_youtube_data(self, youtube_build: Resource, data: dict) -> dict:
        # Video data extracting
        _video_data = youtube_build.videos().list(
            part='snippet', id=data['video_hash']
        ).execute()['items'][0]['snippet']
        tags = _video_data.get('tags', [])
        category_data = youtube_build.videoCategories().list(
            part='snippet', id=_video_data['categoryId']
        ).execute()['items'][0]
        video_statistic = youtube_build.videos().list(
            part='statistics', id=data['video_hash']
        ).execute()['items'][0]['statistics']
        print(video_statistic)

        # Channel data extracting
        channel_data = youtube_build.channels().list(
            part='brandingSettings', id=data['channel_hash']
        ).execute()['items'][0]['brandingSettings']['channel']
        source_data = youtube_build.channels().list(
            part='topicDetails', id=data['channel_hash']
        ).execute()['items'][0]['topicDetails']

        return {
            'video': {
                'tags': tags,
                'youtube_data': {
                    'comment_count': video_statistic.get('commentCount', 0),
                    'positive_mark_number': video_statistic.get('likeCount', 0),
                    'negative_mark_number': video_statistic.get('dislikeCount', 0),
                    'view_count': video_statistic.get('viewCount', 0)
                },
                'category': {
                    'youtube_id': category_data['id'],
                    'etag': category_data['etag'],
                    'name': category_data['snippet']['title'].encode('utf-8').decode('iso-8859-1')
                }
            },
            'channel': {
                'details': {
                    'description': channel_data['description'].encode('utf-8').decode('iso-8859-1'),
                    'country': channel_data.get('country', ''),
                    'keywords': channel_data.get('keywords', '')
                },
                'sources': [
                    name[name.find('/wiki/') + 6:] for name in source_data['topicCategories']
                ]
            }
        }

    def _store_results(self, video, youtube_fetching_result):
        Channel.objects.filter(
            id=video['channel_id']
        ).update(
            **youtube_fetching_result['channel']['details']
        )
        for source in youtube_fetching_result['channel']['sources']:
            source, _ = Source.objects.get_or_create(
                name=source.lower().strip()
            )
            ChannelSource.objects.get_or_create(
                channel_id=video['channel_id'],
                source_id=source.id
            )

        for tag in youtube_fetching_result['video']['tags']:
            tag_object, _ = Tag.objects.get_or_create(
                name=tag.lower().strip()
            )
            TagVideo.objects.get_or_create(
                video_id=video['video_id'],
                tag_id=tag_object.id
            )

        YoutubeData.objects.filter(
            id=video['youtube_data_id']
        ).update(
            **youtube_fetching_result['video']['youtube_data']
        )
        category, _ = Category.objects.get_or_create(
            **youtube_fetching_result['video']['category']
        )
        Video.objects.filter(
            id=video['video_id']
        ).update(
            category_id=category.id,
            status=Video.VideoStatus.CHECKED
        )

    def _handle(self, *args, **options):
        videos = self._fetch_video_data()
        # TODO:::implement in future
        # self._make_video_status_in_progress(
        #     [v.video_id for v in videos]
        # )
        for video in videos:
            credentials = self._fetch_credentials(video)
            if not credentials:
                YoutubeCredentials.objects.filter(id=video['youtube_id']).delete()
                logger.warning('YouTube credentials were invalid for user with id %s', video['user_id'])
                continue

            youtube_build = build("youtube", "v3", credentials=credentials)
            youtube_fetching_result = self._fetch_all_youtube_data(youtube_build, video)

            self._store_results(
                video=video, youtube_fetching_result=youtube_fetching_result
            )
            transaction.commit()

    def handle(self, *args, **options):
        transaction.set_autocommit(False)

        while True:
            try:
                self._handle(*args, **options)
                time.sleep(1)
            except Exception as exc:
                logger.error(exc, exc_info=True)
                transaction.rollback()
