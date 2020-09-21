from django.contrib.auth.signals import user_logged_out
from knox import views
from knox.models import AuthToken
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from accounts.serializers import UserSerializer, LoginSerializer, RegisterSerializer

from youtube.models import Featured
from helpers.async_view_mixin import AsyncViewMixin


class GetUserAPIView(AsyncViewMixin, generics.RetrieveAPIView):

    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer

    async def retrieve(self, request, *args, **kwargs):
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
        }, status=status.HTTP_202_ACCEPTED)

    def get_object(self):
        return self.request.user


class LoginAPIView(AsyncViewMixin, generics.GenericAPIView):
    serializer_class = LoginSerializer
    permissions_classes = [
        permissions.AllowAny
    ]

    async def post(self, request, *a, **kw):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        return Response({
            "data": {
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "token": f'{AuthToken.objects.create(user)[1]}',
            }
        })


class LogoutAPIView(AsyncViewMixin, views.LogoutView):

    async def post(self, request, format=None):
        request._auth.delete()
        user_logged_out.send(sender=request.user.__class__, request=request, user=request.user)
        return Response({
            'data': {
                'message': 'User has logged out successfully!'
            }
        }, status=status.HTTP_200_OK)


class RegisterAPIView(AsyncViewMixin, generics.GenericAPIView):

    serializer_class = RegisterSerializer
    permission_classes = [
        permissions.AllowAny
    ]

    async def post(self, request, *a, **k):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "data": {
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "token": f'{AuthToken.objects.create(user)[1]}',
                'links': []
            }
        })
