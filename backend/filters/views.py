from rest_framework import permissions, generics
from rest_framework.response import Response

from filters.serializers import SourceSerializer, TagSerializer, CategorySerializer
from filters.models import Source, Tag, Category


def _find_filter_by_name(model, name):
    return model.objects.filter(name__contains=name).all()


class SourceAPIView(generics.GenericAPIView):
    serializer_class = SourceSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get(self, request):
        data = _find_filter_by_name(
            model=Source,
            name=request.query_params['name']
        )
        serializer = self.get_serializer(data=data, many=True)
        serializer.is_valid()

        return Response({
            'data': serializer.data
        })


class TagAPIView(generics.GenericAPIView):
    serializer_class = TagSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get(self, request):
        data = _find_filter_by_name(
            model=Tag,
            name=request.query_params['name']
        )
        serializer = self.get_serializer(data=data, many=True)
        serializer.is_valid()

        return Response({
            'data': serializer.data
        })


class CategoryAPIView(generics.GenericAPIView):
    serializer_class = CategorySerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get(self, request):
        data = _find_filter_by_name(
            model=Category,
            name=request.query_params['name']
        )
        serializer = self.get_serializer(data=data, many=True)
        serializer.is_valid()

        return Response({
            'data': serializer.data
        })
