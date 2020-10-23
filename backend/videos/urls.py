from django.urls import path, include
from rest_framework.routers import DefaultRouter

from videos.views import UserMarkAPIView, VideoAPIViewSet, FeaturedAPIView, \
    FeaturedListAPIView


video_urls_router = DefaultRouter()
video_urls_router.register(
    r'', VideoAPIViewSet, basename='video'
)

urlpatterns = [
    path('featured/', FeaturedListAPIView.as_view()),
    path('', include(video_urls_router.urls)),
    path('<int:video_id>/setMark/', UserMarkAPIView.as_view()),
    path('<int:video_id>/featured/', FeaturedAPIView.as_view())
]
