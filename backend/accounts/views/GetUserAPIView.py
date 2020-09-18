from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from ..serializers import UserSerializer, LoginSerializer
from youtube_media.models import Featured


class GetUserAPIView(generics.RetrieveAPIView):

    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        featured_list = [
            x.link.video_id for x in Featured.objects.filter(user=request.user)
        ]        

        return Response({
            'data': {
                'user': serializer.data,
                'links': featured_list
            }
        }, status=status.HTTP_202_ACCEPTED)

    def get_object(self):
        return self.request.user
