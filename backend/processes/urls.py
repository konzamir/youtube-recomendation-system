from django.urls import path, include
from rest_framework.routers import DefaultRouter

from processes.views import ProcessAPIView


urls_router = DefaultRouter()
urls_router.register(
    r'', ProcessAPIView, basename='process'
)

urlpatterns = [
    path('', include(urls_router.urls))
]
