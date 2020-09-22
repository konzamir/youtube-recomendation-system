from django.urls import path, include

from videos.views import UserMarkAPIView


urlpatterns = [
    path('<int:video_id>/', include([
        path('setMark/', UserMarkAPIView.as_view()),
        # path('', ),
    ]))
]
