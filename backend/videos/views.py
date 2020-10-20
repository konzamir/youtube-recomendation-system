from rest_framework import generics, status, permissions, mixins, viewsets
from rest_framework.response import Response

from videos.models import Video, Featured, UserMark, YoutubeData
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
        video = self.get_object()
        serialized_data = self.get_serializer(video).data

        # TODO compute middle sum value in the DB
        user_marks = UserMark.objects.filter(video_id=video.id).values().all()
        marks_len = len(user_marks)

        try:
            current_mark = UserMark.objects.get(user_id=request.user.id)
            current_mark = UserMarkSerializer(current_mark).data
        except UserMark.DoesNotExist:
            current_mark = None

        return Response({
            'data': {
                'video': serialized_data,
                'current_mark': current_mark,
                'user_marks': {
                    'information_quality': sum([x['information_quality'] for x in user_marks]) / marks_len,
                    'medical_practice_quality': sum([x['medical_practice_quality'] for x in user_marks]) / marks_len,
                    'description_quality': sum([x['description_quality'] for x in user_marks]) / marks_len,
                },
                'youtube_marks': {
                    'positive_mark_number': serialized_data['youtube_data']['positive_mark_number'],
                    'negative_mark_number': serialized_data['youtube_data']['negative_mark_number'],
                    'view_count': serialized_data['youtube_data']['view_count'],
                    'comment_count': serialized_data['youtube_data']['comment_count'],

                },
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

    def post(self, request, video_id, *args, **kwargs):
        created, _ = Featured.objects.get_or_create(
            video_id=video_id,
            user_id=request.user.id
        )

        return Response({
            'data': {
                'featured': {
                    'id': created.id,
                    'video_id': video_id,
                    'user_id': request.user.id
                }
            }
        }, status.HTTP_201_CREATED)

    def delete(self, request, video_id, *args, **kwargs):
        Featured.objects.filter(
            video_id=video_id,
            user_id=request.user.id
        ).delete()

        return Response({
            'data': {}
        }, status=status.HTTP_204_NO_CONTENT)
