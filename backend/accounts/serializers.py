from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=64)
    password = serializers.CharField(max_length=64)

    def validate(self, attrs):
        user = authenticate(**attrs)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect credentionals!")


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'password'
        )
        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'username': {
                'required': True
            },
            'email': {
                'required': True
            },
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'], validated_data['email'],
            validated_data['password'])

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')
