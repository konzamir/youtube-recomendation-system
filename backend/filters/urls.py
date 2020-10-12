from django.urls import path

from filters.views import SourceAPIView, TagAPIView, CategoryAPIView


urlpatterns = [
    path('source/', SourceAPIView.as_view()),
    path('tag/', TagAPIView.as_view()),
    path('category/', CategoryAPIView.as_view())
]
