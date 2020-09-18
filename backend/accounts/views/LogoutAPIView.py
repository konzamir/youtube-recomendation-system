from knox import views
from django.contrib.auth.signals import user_logged_in, user_logged_out
from rest_framework import status, permissions
from rest_framework.response import Response


class LogoutAPIView(views.LogoutView):

    def post(self, request, format=None):
        request._auth.delete()
        user_logged_out.send(sender=request.user.__class__,
                            request=request, user=request.user)
        return Response({
            'data': {
                'message': 'User has logged out successfully!'
            }
        }, status=status.HTTP_200_OK)
