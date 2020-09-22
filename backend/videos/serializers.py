from rest_framework import serializers
from videos.models import UserMark


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
        if attrs.get('information_quality') is None or \
                attrs.get('medical_practice_quality') is None or \
                attrs.get('description_quality') is None:
            raise serializers.ValidationError(
                'information_quality or medical_practice_quality '
                'or description_quality should be provided!'
            )

        return attrs
