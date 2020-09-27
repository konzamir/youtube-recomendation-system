from rest_framework import generics, permissions, status
from rest_framework.response import Response

from processes.serializers import ProcessSerializer


class ProcessAPIView(generics.GenericAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = ProcessSerializer

    def post(self, request):
        process_data = request.data
        process_data['user'] = request.user.id

        serializer = self.get_serializer(data=process_data)
        serializer.is_valid(raise_exception=True)
        process = serializer.save()

        return Response({
            'data': {
                'process': self.get_serializer(process, context=self.get_serializer_context()).data,
            }
        }, status=status.HTTP_202_ACCEPTED)
