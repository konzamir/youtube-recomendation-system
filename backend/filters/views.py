from rest_framework import generics, status, permissions
from rest_framework.response import Response

from filters.models import Source, Category
from filters.serializers import FilterDataSerializer


class FiltersAPIView(generics.GenericAPIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    serializer_class = FilterDataSerializer

    def get(self, request):
        # TODO:::replace with a single request
        categories = self.get_serializer(data=Category.objects.all(), many=True)
        categories.is_valid()

        source = self.get_serializer(data=Source.objects.all(), many=True)
        source.is_valid()

        return Response({
            'data': {
                'categories': categories.data,
                'source': source.data
            }
        }, status=status.HTTP_200_OK)
