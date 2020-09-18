from django.conf.urls import url
from .views import GetMediaListAPIView, FeaturedMediaAPIViewSet
from rest_framework import routers


urlpatterns = [
    url(r'^api/get-media/$', GetMediaListAPIView.as_view()),
    url(r'^api/featured/$', FeaturedMediaAPIViewSet.as_view(
    {'get':"list", 'post':"create", 'delete':'destroy'}))
]
#
# router = routers.DefaultRouter()
# router.register(r'api/featured', FeaturedMediaAPIViewSet, 'api-featured')
#
# urlpatterns += router.urls
