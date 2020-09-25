import json
import pytz
from typing import Union
from urllib.parse import urlparse, parse_qs

import aniso8601
from django.conf import settings
from django.contrib.auth.signals import user_logged_out
from django.forms.models import model_to_dict
from django.shortcuts import redirect
from django.urls import reverse
from google_auth_oauthlib.flow import InstalledAppFlow
from oauthlib.oauth2.rfc6749.errors import InvalidGrantError
from knox import views
from knox.models import AuthToken
from rest_framework import generics, permissions
from rest_framework import status
from rest_framework.response import Response

from accounts.serializers import UserSerializer, LoginSerializer, RegisterSerializer
from accounts.models import YoutubeCredentials
from videos.models import Featured
from helpers import is_user_youtube_auth_valid


class GetUserAPIView(generics.GenericAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer

    def get(self, request):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        featured_list = [
            x.link.video_id for x in Featured.objects.filter(user=request.user)
        ]

        return Response({
            'data': {
                'user': serializer.data,
                'links': featured_list
            }
        }, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response({
            'data': {
                'user': serializer.data,
            }
        }, status=status.HTTP_200_OK)


class YoutubeAuthAPIView(generics.GenericAPIView):
    """ This class is for using for storing the youtube auth keys """
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]

    def _parse_credentials(self, credentials: str) -> dict:
        credentials = json.loads(credentials)
        credentials['expiry'] = aniso8601.parse_datetime(
            credentials['expiry']
        ).astimezone(
            pytz.UTC
        ).replace(
            tzinfo=None
        )
        del credentials['scopes']

        return credentials

    def get(self, request):
        flow = InstalledAppFlow.from_client_config(
            settings.YOUTUBE_SECRET,
            scopes=settings.YOUTUBE_SCOPES
        )
        flow.redirect_uri = request.build_absolute_uri(reverse('confirm-youtube-auth'))
        authorization_response = request.build_absolute_uri().replace('http', 'https')

        try:
            flow.fetch_token(authorization_response=authorization_response)
            credentials = flow.credentials.to_json()
            credentials = self._parse_credentials(credentials)
        except InvalidGrantError:
            credentials = None

        if credentials:
            YoutubeCredentials.objects.filter(
                client_id=credentials['client_id']
            ).update(**credentials)
            request.session['success-youtube-auth'] = True
            return redirect('/')

        request.session['success-youtube-auth'] = False
        return redirect('/')


def youtube_link_or_none(request, user) -> Union[str, None]:
    try:
        credentials_from_db = YoutubeCredentials.objects.get(user_id=user.id)
    except YoutubeCredentials.DoesNotExist:
        credentials_from_db = None

    if credentials_from_db is not None and \
            is_user_youtube_auth_valid(model_to_dict(credentials_from_db)):
        return None

    flow = InstalledAppFlow.from_client_config(
        settings.YOUTUBE_SECRET,
        scopes=settings.YOUTUBE_SCOPES
    )

    flow.redirect_uri = request.build_absolute_uri(reverse('confirm-youtube-auth'))
    youtube_link = flow.authorization_url()
    client_id = parse_qs(urlparse(youtube_link[0]).query)['client_id'][0]

    if credentials_from_db is not None:
        credentials_from_db.client_id = client_id
        credentials_from_db.save()
    else:
        YoutubeCredentials(
            user=user,
            client_id=client_id
        ).save()

    return youtube_link[0]


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permissions_classes = [
        permissions.AllowAny
    ]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        featured_list = [
            x.video for x in Featured.objects.filter(user=request.user.id)
        ]

        return Response({
            "data": {
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "token": f'{AuthToken.objects.create(user)[1]}',
                'links': featured_list,
                'youtube_link': youtube_link_or_none(request, user)
            }
        })


class LogoutAPIView(views.LogoutView):

    def post(self, request, format=None):
        request._auth.delete()
        user_logged_out.send(sender=request.user.__class__, request=request, user=request.user)
        return Response({
            'data': {
                'message': 'User has logged out successfully!'
            }
        }, status=status.HTTP_200_OK)


class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [
        permissions.AllowAny
    ]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "data": {
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "token": f'{AuthToken.objects.create(user)[1]}',
                'links': [],
                'youtube_link': youtube_link_or_none(request, user)
            }
        })
