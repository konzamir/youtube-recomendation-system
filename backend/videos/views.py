from rest_framework import generics, status, permissions
from rest_framework.response import Response

from videos.serializers import UserMarkSerializer


class UserMarkAPIView(generics.GenericAPIView):
    serializer_class = UserMarkSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def post(self, request, video_id):
        user_mark_data = request.data
        user_mark_data['video_id'] = video_id
        serializer = self.get_serializer(data=user_mark_data)
        serializer.is_valid(raise_exception=True)
        user_mark = serializer.save()

        return Response({
            'data': {
                'user_mark': self.get_serializer(user_mark, context=self.get_serializer_context()).data,
            }
        }, status=status.HTTP_202_ACCEPTED)
