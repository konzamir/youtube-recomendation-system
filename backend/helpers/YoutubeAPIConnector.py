import requests
from django.conf import settings
import hashlib


class YoutubeAPIConnector:

    _main_url = "https://content.googleapis.com/youtube/v3/search?"
    _headers = {
        'part': 'snippet',
        'key': settings.YOUTUBE_API_KEY,
        'q': '',
        'type': 'video',
        'maxResults': 25,
    }

    @classmethod
    def hash_data(cls, data) -> str:
        temp = hashlib.md5(data.encode())
        return temp.hexdigest()

    @classmethod
    def convert_to_valid(cls, data, req_text, full_url) -> dict:
        ctx = {
            'request_data': {},
            'links': [],
        }

        request_data = {
            'click_count': 0,
            'data': req_text,
            'hash_data': cls.hash_data(req_text),
            'full_url': full_url,
            'region': data['regionCode'],
            'etag': data['etag'],
            'next_page': data.get('nextPageToken', None),
            'prev_page': data.get('prevPageToken', None)
        }

        links = []

        for x in data['items']:
            t = x['snippet']['thumbnails']["high"]

            link = {
                'etag': x['etag'],
                'published_at': x['snippet']['publishedAt'],
                'channel_id': x['snippet']['channelId'],
                'video_id': x['id']['videoId'],
                'title': x['snippet']['title'],
                'description': x['snippet']['description'],
                'channel_title': x['snippet']['channelTitle'],

                'preview_url': t['url'],
                'width': t['width'],
                'height': t['height'],
            }

            links.append(link)

        ctx['request_data'] = request_data
        ctx['links'] = links

        return ctx

    @classmethod
    def send_request(cls, q, max_results=25, page_token=None, region_code=None):
        headers = cls._headers
        if page_token:
            headers['pageToken'] = page_token
        if region_code:
            headers['regionCode'] = region_code
        headers['maxResults'] = max_results
        headers['q'] = q

        r = requests.get(url=cls._main_url, params=headers)
        return cls.convert_to_valid(data=r.json(), req_text=q, full_url=r.url)
