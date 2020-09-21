from django.urls import path, include

from accounts.views import RegisterAPIView, LoginAPIView, GetUserAPIView, LogoutAPIView


urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view(), name='knox-logout'),
    path('auth', include('knox.urls')),
    path('user/', GetUserAPIView.as_view()),
]
