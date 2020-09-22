from rest_framework import serializers

from filters.models import Source, Destination, \
    VideoType


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = '__all__'


class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = '__all__'


class VideoTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoType
        fields = '__all__'


class FilterDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = '__all__'
