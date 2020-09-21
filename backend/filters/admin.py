from django.contrib import admin
from filters.models import Source, Destination, VideoType, \
    UserMark


admin.site.register(Source)
admin.site.register(Destination)
admin.site.register(VideoType)
admin.site.register(UserMark)
