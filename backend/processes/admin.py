from django.contrib import admin
from processes.models import Process, ProcessVideo, ProcessTag, ProcessSource, ProcessCategory


admin.site.register(ProcessVideo)
admin.site.register(Process)
admin.site.register(ProcessTag)
admin.site.register(ProcessCategory)
admin.site.register(ProcessSource)
