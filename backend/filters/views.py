from rest_framework import generics, status, permissions
from rest_framework.response import Response

from filters.models import VideoType, Source, Destination
from filters.serializers import FilterDataSerializer


class FiltersAPIView(generics.GenericAPIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    serializer_class = FilterDataSerializer

    def get(self, request):
        queryset = VideoType.objects | Destination.objects | Source.objects
        print(queryset.all())
        serialized_data = self.get_serializer(data=queryset.all(), many=True)

        return Response({
            'data': {
                'tempo': serialized_data
            }
        }, status=status.HTTP_200_OK)