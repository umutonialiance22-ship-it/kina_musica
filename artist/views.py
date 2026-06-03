from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema
from .models import ArtistStat, ChannelLink, TrendAlert
from .serializers import ArtistStatSerializer, ChannelLinkSerializer, TrendAlertSerializer

@extend_schema(tags=['ARTIST'])
class ArtistStatView(generics.RetrieveUpdateAPIView):
    serializer_class = ArtistStatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        stat, created = ArtistStat.objects.get_or_create(artist=self.request.user)
        return stat

@extend_schema(tags=['ARTIST'])
class ChannelLinkListCreateView(generics.ListCreateAPIView):
    serializer_class = ChannelLinkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChannelLink.objects.filter(artist=self.request.user)

    def perform_create(self, serializer):
        serializer.save(artist=self.request.user)

@extend_schema(tags=['ARTIST'])
class TrendAlertListView(generics.ListAPIView):
    serializer_class = TrendAlertSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TrendAlert.objects.filter(artist=self.request.user).order_by('-created_at')

