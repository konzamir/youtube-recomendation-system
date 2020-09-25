from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def test(request, *args, **kwargs):
    return JsonResponse({
        'args': args,
        'kwargs': kwargs,
        'success': request.session['success-youtube-auth']
    })


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include([
        path('auth/', include('accounts.urls')),
        path('filters/', include('filters.urls')),
        path('videos/', include('videos.urls')),
        path('processes/', include('processes.urls'))
    ])),
    path('', test)
]
