from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema
from .models import Favorite, History, Recording, Follower, Comment, Review
from .serializers import (FavoriteSerializer, HistorySerializer, 
    RecordingSerializer, FollowerSerializer, CommentSerializer, ReviewSerializer)

@extend_schema(tags=['FAN'])
class FavoriteListCreateView(generics.ListCreateAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(fan=self.request.user)

    def perform_create(self, serializer):
        serializer.save(fan=self.request.user)

@extend_schema(tags=['FAN'])
class HistoryListView(generics.ListAPIView):
    serializer_class = HistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return History.objects.filter(fan=self.request.user).order_by('-played_at')

@extend_schema(tags=['FAN'])
class RecordingListCreateView(generics.ListCreateAPIView):
    serializer_class = RecordingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Recording.objects.filter(fan=self.request.user)

    def perform_create(self, serializer):
        serializer.save(fan=self.request.user)

@extend_schema(tags=['FAN'])
class FollowerListCreateView(generics.ListCreateAPIView):
    serializer_class = FollowerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Follower.objects.filter(fan=self.request.user)

    def perform_create(self, serializer):
        serializer.save(fan=self.request.user)

@extend_schema(tags=['FAN'])
class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        song_id = self.request.query_params.get('song_id')
        return Comment.objects.filter(song_id=song_id)

    def perform_create(self, serializer):
        serializer.save(fan=self.request.user)

@extend_schema(tags=['FAN'])
class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(fan=self.request.user)

    def perform_create(self, serializer):
        serializer.save(fan=self.request.user)

