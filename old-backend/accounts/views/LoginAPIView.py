from ..serializers import LoginSerializer, UserSerializer
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from youtube_media.models import Featured


class LoginAPIView(generics.GenericAPIView):
    
    serializer_class = LoginSerializer
    permissions_classes = [
        permissions.AllowAny
    ]

    def post(self, request, *a, **kw):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        return Response({
            "data": {
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "token": f'{AuthToken.objects.create(user)[1]}',
            }
        })
