from rest_framework import (
    permissions, status, mixins, viewsets, exceptions)
from rest_framework.response import Response
from ..serializers import LinkSerializer
from ..models import Featured, Links
from ..tasks import featured_links
from exceptions import NoVideoIdException


class FeaturedMediaAPIViewSet(mixins.CreateModelMixin,
                              mixins.DestroyModelMixin,
                              mixins.ListModelMixin,
                              viewsets.GenericViewSet):

    serializer_class = LinkSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]
    queryset = Links.objects.all()

    async def __call__(self, *args, **kwargs):
        return super(FeaturedMediaAPIViewSet, self).__call__(*args, **kwargs)

    def check_video_id(self, request):
        if request.data.get('video_id', None) is None:
            raise NoVideoIdException(detail="No video id were found!")

    def list(self, request, *args, **kwargs):
        featured_list = Featured.objects.filter(user=request.user)
        links = [x.link for x in featured_list]

        links_serializer = self.get_serializer(links, many=True, context=self.get_serializer_context())

        return Response({
            'data': {
                'links': links_serializer.data
            }
        }, status=status.HTTP_202_ACCEPTED)

    def create(self, request, *args, **kwargs):
        self.check_video_id(request)

        ctx = {
            'video_id': request.data.get('video_id'),
            'user_id': request.user.id
        }
        featured_links.delay(ctx, True)

        return Response({
            'data': {
                'message': "Is saving!"
            }
        }, status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        self.check_video_id(request)
        ctx = {
            'video_id': request.data.get('video_id'),
            'user_id': request.user.id
        }
        featured_links.delay(ctx, False)
        return Response({
            'data': {
                'message': "Is removing!"
            }
        }, status.HTTP_204_NO_CONTENT)
