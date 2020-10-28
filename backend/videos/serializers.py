from rest_framework import serializers

from videos.models import UserMark, ImagePreview, YoutubeData, \
    Video
from filters.serializers import CategorySerializer


class ImagePreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagePreview
        fields = '__all__'


class YoutubeDataSerializer(serializers.ModelSerializer):
    image_preview = ImagePreviewSerializer(many=False, read_only=True)

    class Meta:
        model = YoutubeData
        fields = '__all__'


class SmallYoutubeDataSerializer(serializers.ModelSerializer):
    image_preview = ImagePreviewSerializer(many=False, read_only=True)

    class Meta:
        model = YoutubeData
        fields = ('image_preview', )


class SmallVideoSerializer(serializers.ModelSerializer):
    youtube_data = SmallYoutubeDataSerializer(many=False)

    class Meta:
        model = Video
        fields = ('id', 'title', 'description', 'youtube_data')


class VideoSerializer(serializers.ModelSerializer):
    youtube_data = YoutubeDataSerializer(many=False)

    class Meta:
        model = Video
        fields = '__all__'


class UserMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMark
        fields = '__all__'
        extra_kwargs = {
            'information_quality': {
                'required': False
            },
            'medical_practice_quality': {
                'required': False
            },
            'description_quality': {
                'required': False
            },
            'practical_usage_availability': {
                'required': False
            },
            'video': {
                'write_only': True
            },
            'user': {
                'write_only': True
            },
        }

    def validate(self, attrs):
        if attrs.get('information_quality') is None and \
                attrs.get('medical_practice_quality') is None and \
                attrs.get('description_quality') is None:
            raise serializers.ValidationError(
                'information_quality or medical_practice_quality '
                'or description_quality should be provided!'
            )

        return attrs
