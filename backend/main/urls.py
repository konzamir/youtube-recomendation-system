from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include([
        path('auth/', include('accounts.urls')),
        path('videos/', include('videos.urls')),
        path('processes/', include('processes.urls')),
        path('filters/', include('filters.urls'))
    ])),
]
