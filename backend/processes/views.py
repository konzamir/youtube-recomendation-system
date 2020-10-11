from django.db import transaction
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from processes.serializers import ProcessSerializer
from processes.models import ProcessTag, ProcessCategory, ProcessSource


class ProcessAPIView(generics.GenericAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = ProcessSerializer

    def post(self, request):
        process_data = request.data['process']
        process_data['user'] = request.user.id

        serializer = self.get_serializer(data=process_data)
        serializer.is_valid(raise_exception=True)
        process = serializer.save()

        with transaction.atomic():
            for tag_id in request.data['tags']:
                ProcessTag.objects.create(
                    process_id=process.id,
                    tag_id=tag_id
                )

            for category_id in request.data['categories']:
                ProcessCategory.objects.create(
                    process_id=process.id,
                    category_id=category_id
                )

            for source_id in request.data['sources']:
                ProcessSource.objects.create(
                    process_id=process.id,
                    tag_id=source_id
                )

        return Response({
            'data': {
                'process': self.get_serializer(process, context=self.get_serializer_context()).data,
            }
        }, status=status.HTTP_202_ACCEPTED)
