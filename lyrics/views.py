from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema
from .models import Lyric
from .serializers import LyricsSerializer

@extend_schema(tags=['LYRICS'])
class LyricsDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = LyricsSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        return Lyric.objects.get(song_id=self.kwargs['song_id'])