from rest_framework import serializers
from youtube.models import Video


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        exclude = ('updated_at', 'created_at')
