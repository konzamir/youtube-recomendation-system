from rest_framework import serializers

from filters.models import Category, Source


class FilterDataSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=64)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = '__all__'
