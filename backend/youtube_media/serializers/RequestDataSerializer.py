from rest_framework import serializers
from ..models import RequestData


class RequestDataSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = RequestData
        # fields = ('id', 'data', 'next_page', 'prev_page')
        exclude = ('id', 'updated_at', 'created_at', 'etag',
                   'hash_data', 'full_url', 'region')
