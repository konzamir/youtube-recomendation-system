from django.contrib import admin

from videos.models import Channel, ImagePreview, YoutubeData, \
    Video, Featured, UserMark, Tag, Source, Category


admin.site.register(Channel)
admin.site.register(ImagePreview)
admin.site.register(YoutubeData)
admin.site.register(Video)
admin.site.register(Featured)
admin.site.register(UserMark)
admin.site.register(Tag)
admin.site.register(Source)
admin.site.register(Category)

