from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema
from .models import Album
from .serializers import AlbumSerializer

# Create your views here.
@extend_schema(tags=['ALBUMS'])
class AlbumListCreateView(generics.ListCreateAPIView):
    serializer_class = AlbumSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Album.objects.filter(artist=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(artist=self.request.user)

@extend_schema(tags=['ALBUMS'])
class AlbumDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AlbumSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Album.objects.filter(artist=self.request.user)        
