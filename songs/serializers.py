from rest_framework import serializers
from .models import Song


class SongSerializer(serializers.ModelSerializer):
    artist_name = serializers.SerializerMethodField()  # ✅ shows artist name not just ID
    lyrics = serializers.SerializerMethodField()        # ✅ includes lyrics in song response

    class Meta:
        model = Song
        fields = '__all__'
        read_only_fields = ['id', 'artist', 'uploaded_at', 'total_streams']

    def get_artist_name(self, obj):
        return f"{obj.artist.first_name} {obj.artist.last_name}".strip() or obj.artist.username

    def get_lyrics(self, obj):
        try:
            return {
                'plain_lyrics': obj.lyric.plain_lyrics,
                'synced_lrc': obj.lyric.synced_lrc,
                'source': obj.lyric.source,
            }
        except:
            return None