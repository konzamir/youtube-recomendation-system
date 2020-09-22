from django.urls import path
from processes.views import ProcessAPIView


urlpatterns = [
    path('create/', ProcessAPIView.as_view())
]
