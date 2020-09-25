import pytz

import aniso8601
from django.core.management.base import BaseCommand
from django.conf import settings
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


class Command(BaseCommand):
    help = ''

    # def add_arguments(self, parser: CommandParser):
    #     pass

    def handle(self, *args, **options):
        json_credentials = {}
        if 'id' in credentials_from_db:
            del credentials_from_db['id']
        if 'user' in credentials_from_db:
            del credentials_from_db['user']

        json_credentials['expiry'] = aniso8601.parse_datetime(
            json_credentials['expiry']
        ).astimezone(
            pytz.UTC
        ).replace(
            tzinfo=None
        )
        new_credentials = Credentials(**json_credentials)

        youtube = build("youtube", "v3", credentials=new_credentials)
        # print(youtube.channels().list(part='statistics', forUsername='konzamir').execute())
        print(youtube.search().list(part='snippet', type='video', q='test', maxResults=25).execute())
