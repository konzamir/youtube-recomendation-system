from django.urls import path

from filters.views import FiltersAPIView

urlpatterns = [
    path('', FiltersAPIView.as_view())
]