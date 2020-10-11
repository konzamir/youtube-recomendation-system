from django.contrib import admin

from filters.models import Source, Tag, Category


admin.site.register(Source)
admin.site.register(Tag)
admin.site.register(Category)
