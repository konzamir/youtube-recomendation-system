from rest_framework import generics, permissions, exceptions
from rest_framework.response import Response
from knox.models import AuthToken
from ..serializers import UserSerializer, RegisterSerializer
from youtube_media.models import Featured


class RegisterAPIView(generics.GenericAPIView):

    serializer_class = RegisterSerializer
    permission_classes = [
        permissions.AllowAny
    ]

    def post(self, request, *a, **k):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # featured_list = [
        #     x.link.video_id for x in Featured.objects.filter(user=user)
        # ]

        return Response({
            "data": {
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "token": f'{AuthToken.objects.create(user)[1]}',
                'links': []
            }
        })
