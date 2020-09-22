from rest_framework import generics, status, permissions, mixins, viewsets
from rest_framework.response import Response

from videos.models import Video
from videos.serializers import UserMarkSerializer, VideoSerializer


class VideoAPIViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = VideoSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_queryset(self):
        # TODO:::upgrade queryset if would be necessary
        return Video.objects.all()

    def list(self, request, *args, **kwargs):
        response = super(VideoAPIViewSet, self).list(request, *args, **kwargs)

        return Response({
            'data': {
                'videos': response.data
            }
        })

    def retrieve(self, request, *args, **kwargs):
        response = super(VideoAPIViewSet, self).retrieve(request, *args, **kwargs)

        return Response({
            'data': {
                'video': response.data
            }
        })


class UserMarkAPIView(generics.GenericAPIView):
    serializer_class = UserMarkSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def post(self, request, video_id):
        user_mark_data = request.data
        user_mark_data['video'] = video_id
        user_mark_data['user'] = request.user.id

        serializer = self.get_serializer(data=user_mark_data)
        serializer.is_valid(raise_exception=True)
        user_mark = serializer.save()

        return Response({
            'data': {
                'user_mark': self.get_serializer(
                    user_mark,
                    context=self.get_serializer_context()
                ).data,
            }
        }, status=status.HTTP_202_ACCEPTED)
