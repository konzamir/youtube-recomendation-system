from rest_framework import serializers

from videos.models import UserMark, Channel, ImagePreview, YoutubeData, \
    Video
# from filters.serializers import SourceSerializer, CategorySerializer, TagSerializer


class ChannelSerializer(serializers.ModelSerializer):
    # source = SourceSerializer(many=False, read_only=True)

    class Meta:
        model = Channel
        fields = '__all__'


class ImagePreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagePreview
        fields = '__all__'


class YoutubeDataSerializer(serializers.ModelSerializer):
    image_preview = ImagePreviewSerializer(many=False, read_only=True)

    class Meta:
        model = YoutubeData
        fields = '__all__'


class VideoSerializer(serializers.ModelSerializer):
    channel = ChannelSerializer(many=False)
    youtube_data = YoutubeDataSerializer(many=False)
    # category = CategorySerializer(many=False)

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
            }
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
