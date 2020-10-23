from django.db.utils import IntegrityError
from rest_framework import generics, status, permissions, mixins, viewsets
from rest_framework.response import Response

from videos.models import Video, Featured, UserMark
from videos.serializers import UserMarkSerializer, VideoSerializer, SmallVideoSerializer


def _get_quality_value(field_key, user_marks):
    curr_len = len(
        [x[field_key] for x in user_marks if x[field_key] > 0]
    ) or 1
    return round(
        sum([x[field_key] for x in user_marks]) / curr_len,
        2
    )



class VideoAPIViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = VideoSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_queryset(self):
        return Video.objects.select_related('youtube_data').all()

    def retrieve(self, request, *args, **kwargs):
        video = self.get_object()
        serialized_data = self.get_serializer(video).data

        # TODO:::compute middle sum value in the DB
        user_marks = UserMark.objects.filter(video_id=video.id).values().all()

        try:
            # TODO:::reduce number of requests to the DB
            current_mark = UserMark.objects.get(user_id=request.user.id, video_id=video.id)
            current_mark = UserMarkSerializer(current_mark).data
        except UserMark.DoesNotExist:
            current_mark = {}

        return Response({
            'data': {
                'video': serialized_data,
                'current_mark': current_mark,
                'user_marks': {
                    'information_quality': _get_quality_value('information_quality', user_marks),
                    'medical_practice_quality': _get_quality_value('medical_practice_quality', user_marks),
                    'description_quality': _get_quality_value('description_quality', user_marks),
                    'practical_usage_availability': _get_quality_value('practical_usage_availability', user_marks),
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
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def post(self, request, video_id):
        user_mark_data = request.data
        user_mark_data['video_id'] = video_id
        user_mark_data['user_id'] = request.user.id

        if 'id' in user_mark_data and not isinstance(user_mark_data['id'], int):
            del user_mark_data['id']

        if user_mark_data.get('id'):
            UserMark.objects.filter(id=user_mark_data['id']).update(
                **user_mark_data
            )
        else:
            try:
                UserMark.objects.create(
                    **user_mark_data
                )
            except IntegrityError:
                UserMark.objects.filter(
                    user_id=user_mark_data['user_id'],
                    video_id=user_mark_data['video_id']
                ).update(
                    **user_mark_data
                )

        current_mark = UserMark.objects.get(
            user_id=user_mark_data['user_id'],
            video_id=user_mark_data['video_id']
        )
        user_marks = UserMark.objects.filter(video_id=video_id).values().all()

        return Response({
            'data': {
                'updated_mark': UserMarkSerializer(current_mark).data,
                'user_marks': {
                    'information_quality': _get_quality_value('information_quality', user_marks),
                    'medical_practice_quality': _get_quality_value('medical_practice_quality', user_marks),
                    'description_quality': _get_quality_value('description_quality', user_marks),
                    'practical_usage_availability': _get_quality_value('practical_usage_availability', user_marks),
                },
            }
        }, status=status.HTTP_202_ACCEPTED)


class FeaturedListAPIView(generics.GenericAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get(self, request, *args, **kwargs):
        videos = Video.objects.filter(
            id__in=Featured.objects.filter(
                user_id=request.user.id,
            ).values('video_id')
        ).all()

        return Response({
            'data': {
                'videos': SmallVideoSerializer(videos, many=True).data
            }
        })


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
