from rest_framework import serializers

from filters.models import Destination, VideoType, Source


class FilterDataSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=64)


class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = '__all__'


class VideoTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoType
        fields = '__all__'


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = '__all__'
