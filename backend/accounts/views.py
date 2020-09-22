from django.contrib.auth.signals import user_logged_out
from knox import views
from knox.models import AuthToken
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status

from accounts.serializers import UserSerializer, LoginSerializer, RegisterSerializer
from videos.models import Featured


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
                'links': featured_list
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
                'links': []
            }
        })
