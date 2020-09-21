from django.contrib import admin
from youtube.models import Channel, ImagePreview, YoutubeData, \
    Video, Featured


admin.site.register(Channel)
admin.site.register(ImagePreview)
admin.site.register(YoutubeData)
admin.site.register(Video)
admin.site.register(Featured)
