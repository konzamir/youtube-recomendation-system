from django.conf.urls import url, include
from .views import RegisterAPIView, LoginAPIView, GetUserAPIView, LogoutAPIView
from knox import views as knox_views


urlpatterns = [
    url(r'api/auth/register/', RegisterAPIView.as_view()),
    url(r'api/auth/login/', LoginAPIView.as_view()),
    url(r'api/auth/logout/', LogoutAPIView.as_view(), name='knox-logout'),
    url(r'api/auth', include('knox.urls')),
    url(r'api/auth/user/', GetUserAPIView.as_view()),
]
