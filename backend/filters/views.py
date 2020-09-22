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
        # TODO:::replace with a single request
        video_types = self.get_serializer(data=VideoType.objects.all(), many=True)
        video_types.is_valid()

        destination = self.get_serializer(data=Destination.objects.all(), many=True)
        destination.is_valid()

        source = self.get_serializer(data=Source.objects.all(), many=True)
        source.is_valid()

        return Response({
            'data': {
                'video_type': video_types.data,
                'destination': destination.data,
                'source': source.data
            }
        }, status=status.HTTP_200_OK)
