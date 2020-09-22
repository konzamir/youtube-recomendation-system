from django.urls import path

from videos.views import UserMarkAPIView


urlpatterns = [
    path('<int:video_id>/setMark', UserMarkAPIView.as_view())
]
