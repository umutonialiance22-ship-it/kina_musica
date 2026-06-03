from rest_framework import serializers
from .models import ArtistStat, ChannelLink, TrendAlert

class ArtistStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistStat
        fields = '__all__'
        read_only_fields = ['id', 'artist', 'updated_at']

class ChannelLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelLink
        fields = '__all__'
        read_only_fields = ['id', 'artist']

class TrendAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrendAlert
        fields = '__all__'
        read_only_fields = ['id', 'artist', 'created_at']
                        