from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = ''

    # def add_arguments(self, parser: CommandParser):
    #     pass

    def handle(self, *args, **options):
        import os
        import pickle

        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build

        credentials = None

        # token.pickle stores the user's credentials from previously successful logins
        # if os.path.exists('token.pickle'):
        #     with open('token.pickle', 'rb') as token:
        #         credentials = pickle.load(token)

        # If there are no valid credentials available, then either refresh the token or log in.
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'client_secret.json',
                    scopes=[
                        'https://www.googleapis.com/auth/youtube.readonly'
                    ]
                )

                flow.run_local_server(port=8000, prompt='consent', authorization_prompt_message='')
                credentials = flow.credentials

                # Save the credentials for the next run
                # with open('token.pickle', 'wb') as f:
                #     pickle.dump(credentials, f)

        import json
        import pytz

        import aniso8601
        from google.oauth2.credentials import Credentials


        json_credentials = json.loads(credentials.to_json())
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
