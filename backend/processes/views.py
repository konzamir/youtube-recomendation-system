from django.db import transaction
from rest_framework import permissions, status, mixins, viewsets
from rest_framework.response import Response

from videos.serializers import SmallVideoSerializer
from videos.models import Video

from processes.serializers import ProcessSerializer
from processes.models import ProcessTag, ProcessCategory, ProcessSource, \
    ProcessVideo, Process


class ProcessAPIView(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = ProcessSerializer
    queryset = Process.objects.all()

    def retrieve(self, request, *args, **kwargs):
        process = self.get_object()
        videos = []

        if process.status == Process.ProcessStatus.SUCCESS:
            videos = Video.objects.filter(
                id__in=ProcessVideo.objects.filter(
                    process_id=process.id,
                    video_order__gt=0
                ).values('video_id')
            ).order_by('pv_videos__video_order').all()

        return Response({
            'data': {
                'process': self.get_serializer(process).data,
                'videos': SmallVideoSerializer(videos, many=True).data
            }
        })

    def create(self, request, *args, **kwargs):
        process_data = request.data['process']
        process_data['user'] = request.user.id
        process_data['active'] = True

        serializer = self.get_serializer(data=process_data)
        serializer.is_valid(raise_exception=True)
        process = serializer.save()

        with transaction.atomic():
            for tag in request.data['tags']:
                ProcessTag.objects.get_or_create(
                    process_id=process.id,
                    tag_id=tag['id']
                )

            for category in request.data['categories']:
                ProcessCategory.objects.get_or_create(
                    process_id=process.id,
                    category_id=category['id']
                )

            for source in request.data['sources']:
                ProcessSource.objects.get_or_create(
                    process_id=process.id,
                    source_id=source['id']
                )

        return Response({
            'data': {
                'process': self.get_serializer(process).data
            }
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        response = super(ProcessAPIView, self).update(request, *args, **kwargs)

        return Response({
            'data': {
                'process': response.data
            }
        }, status=status.HTTP_200_OK)
