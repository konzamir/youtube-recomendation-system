from rest_framework import generics, status, permissions, mixins, viewsets
from rest_framework.response import Response

from videos.models import Video, Featured
from videos.serializers import UserMarkSerializer, VideoSerializer


class VideoAPIViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = VideoSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_queryset(self):
        # TODO:::upgrade queryset with prefetch_related and select_related
        return Video.objects.all()

    def retrieve(self, request, *args, **kwargs):
        response = super(VideoAPIViewSet, self).retrieve(request, *args, **kwargs)

        return Response({
            'data': {
                'video': response.data,
                'user_marks': [],
                'youtube_marks': [],
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


class FeaturedAPIView(generics.GenericAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def post(self, request, video_id):
        Featured.objects.create(
            user_id=request.user.id,
            video_id=video_id
        )
        return Response({
            'data': {
                'msg': 'Success creation!'
            }
        }, status=status.HTTP_202_ACCEPTED)
