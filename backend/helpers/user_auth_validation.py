import pytz

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


def is_user_youtube_auth_valid(credentials_from_db: dict) -> bool:
    # TODO:::add saving after token refreshing
    if not credentials_from_db['token']:
        return False

    if 'id' in credentials_from_db:
        del credentials_from_db['id']
    if 'user' in credentials_from_db:
        del credentials_from_db['user']

    credentials_from_db['expiry'] = credentials_from_db['expiry'].astimezone(
        pytz.UTC).replace(tzinfo=None)

    credentials = Credentials(**credentials_from_db)
    if credentials.valid:
        return True

    if credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
        if credentials.valid:
            return True

    return False
