from rest_framework import serializers
from videos.models import UserMark


class UserMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMark
        fields = '__all__'
