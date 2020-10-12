from django.db import transaction
from rest_framework import permissions, status, mixins, viewsets
from rest_framework.response import Response

from videos.serializers import SmallVideoSerializer
from videos.models import Video

from processes.serializers import ProcessSerializer
from processes.models import ProcessTag, ProcessCategory, ProcessSource, \
    ProcessVideo, Process


class ProcessAPIView(mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
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
                )
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

        serializer = self.get_serializer(data=process_data)
        serializer.is_valid(raise_exception=True)
        process = serializer.save()

        with transaction.atomic():
            for tag_id in request.data['tags']:
                ProcessTag.objects.get_or_create(
                    process_id=process.id,
                    tag_id=tag_id
                )

            for category_id in request.data['categories']:
                ProcessCategory.objects.get_or_create(
                    process_id=process.id,
                    category_id=category_id
                )

            for source_id in request.data['sources']:
                ProcessSource.objects.get_or_create(
                    process_id=process.id,
                    tag_id=source_id
                )

        return Response({
            'data': {
                'process': self.get_serializer(process, context=self.get_serializer_context()).data,
            }
        }, status=status.HTTP_202_ACCEPTED)
