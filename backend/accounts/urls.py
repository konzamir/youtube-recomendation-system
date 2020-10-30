from django.urls import path, include
from rest_framework.routers import DefaultRouter

from accounts.views import RegisterAPIView, LoginAPIView, GetUpdateUserAPIViewSet, YoutubeAuthAPIView

urls_router = DefaultRouter()
urls_router.register(
    r'', GetUpdateUserAPIViewSet, basename='user'
)


urlpatterns = [
    # path('register/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('auth', include('knox.urls')),
    path('user/', include(urls_router.urls)),
    path('youtubeAuth/', YoutubeAuthAPIView.as_view(), name='confirm-youtube-auth')
]
