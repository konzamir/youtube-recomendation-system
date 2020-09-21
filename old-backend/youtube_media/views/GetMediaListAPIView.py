from rest_framework import generics, permissions, exceptions
from rest_framework.response import Response
from ..serializers import *
from helpers import YoutubeAPIConnector
from django.conf import settings
from ..models import RequestData, RequestLinkConn, Links
from ..tasks import save_items
import hashlib


class GetMediaListAPIView(generics.GenericAPIView):

    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = LinkSerializer

    def validate_request_data(self, data) -> dict:
        ctx = data
        
        del ctx['request_data']["hash_data"]
        del ctx['request_data']["full_url"]
        del ctx['request_data']["region"]
        del ctx['request_data']["etag"]
        ctx['request_data']['click_count'] = 1

        for x in ctx['links']:
            del x['etag']
            # x['featured'] = False
        return ctx

    def validate_db_data(self, data) -> dict:
        ctx = data
        
        for x in ctx['links']:
            x['title'] = x['title'].encode('iso-8859-1').decode('utf-8')
            x['description'] = x['description'].encode('iso-8859-1').decode('utf-8')
            x['channel_title'] = x['channel_title'].encode('iso-8859-1').decode('utf-8')
            # x['featured'] = False
        
        return ctx

    def send_request(self, request) -> dict:
        q = request.data.get('q', '')
        ctx = {
            'q': q,
            'max_results': settings.ITEMS_PER_PAGE
        }

        page_token = request.data.get('page_token', None)
        region_code = request.data.get('region_code', None)

        if page_token:
            ctx['page_token'] = page_token
        if region_code:
            ctx['region_code'] = region_code

        media_list = YoutubeAPIConnector.send_request(**ctx)
        media_list['request_data']['curr_page'] = page_token
        save_items.delay(media_list)
        return media_list

    def get_from_db(self, r) -> dict:
        r.click_count += 1
        r.save()

        ctx = {
            'request_data': {},
            'links': [],
        }

        request_serializer = RequestDataSerializer(r).data

        req_link_conns = RequestLinkConn.objects.filter(
            request_data=r)[:int(settings.ITEMS_PER_PAGE)]
        links_serializers = LinkSerializer(
            [x.link for x in req_link_conns], many=True).data

        ctx['request_data'] = request_serializer
        ctx['links'] = links_serializers
        return ctx

    def post(self, request, *a, **kw):
        q = request.data.get('q', '').replace(' ', '+')
        hash_q = hashlib.md5(q.encode()).hexdigest()
        page_token = request.data.get('page_token', None)
        try:
            if page_token:
                r = RequestData.objects.get(hash_data=hash_q, curr_page=page_token)
            else:
                r = RequestData.objects.get(hash_data=hash_q, curr_page__isnull=True)

            if r.click_count > 0:
                data = self.validate_db_data(self.get_from_db(r))
            else:
                data = self.validate_request_data(self.send_request(request))
        except RequestData.DoesNotExist:
            data = self.validate_request_data(self.send_request(request))
        except RequestData.MultipleObjectsReturned:
            raise exceptions.APIException("Not valid input data", 500)

        return Response({'data': data, "error": None})
