from rest_framework import generics, permissions
from .models import Song
from .serializers import SongSerializer
from drf_spectacular.utils import extend_schema

# Create your views here.
@extend_schema(summary="List all songs with filters", tags=['SONGS'])
class SongListView(generics.ListAPIView):
    serializer_class = SongSerializer
    permission_classes = [permissions.AllowAny]

    

    def get_queryset(self):
        queryset = Song.objects.all()
        genre = self.request.query_params.get('genre')
        era = self.request.query_params.get('era')
        difficulty = self.request.query_params.get('difficulty')
        if genre: 
            queryset = queryset.filter(genre__icontains=genre)
        if era:
            queryset = queryset.filter(era=era)
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        return queryset
                
class TrendingSongsView(generics.ListAPIView):
    serializer_class = SongSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Song.objects.order_by('-total_streams')[:10]

    @extend_schema(summary="Get 10 top trending songs", tags=['SONGS'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class LiveSongsView(generics.ListAPIView):
    serializer_class = SongSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Song.objects.filter(is_live=True)

    @extend_schema(
        summary="Get all live songs",
        tags=['SONGS']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class SongUploadView(generics.CreateAPIView):
    serializer_class = SongSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="Upload a new song",
        tags=['SONGS']
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(artist=self.request.user)        
