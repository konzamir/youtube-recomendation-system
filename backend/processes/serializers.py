from rest_framework import serializers
from processes.models import Process


class ProcessSerializer(serializers.ModelSerializer):

    class Meta:
        model = Process
        fields = '__all__'
        extra_kwargs = {
            'youtube_video_group': {
                'required': False
            },
            'user': {
                'write_only': True
            }
        }
