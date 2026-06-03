from rest_framework import serializers
from .models import Lyric

class LyricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lyric
        fields = '__all__'
        read_only_fields = ['id']

