from django.urls import path, include
from rest_framework.routers import DefaultRouter

from videos.views import UserMarkAPIView, VideoAPIViewSet


video_urls_router = DefaultRouter()
video_urls_router.register(
    r'', VideoAPIViewSet, basename='video'
)

urlpatterns = [
    path('', include(video_urls_router.urls)),
    path('<int:video_id>/setMark/', UserMarkAPIView.as_view()),
]
