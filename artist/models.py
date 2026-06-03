from django.db import models
from users.models import User
from songs.models import Song

# Create your models here.
class ArtistStat(models.Model):
    artist = models.OneToOneField(User, on_delete=models.CASCADE, related_name='stats')
    total_streams = models.PositiveIntegerField(default=0)
    total_listeners = models.PositiveIntegerField(default=0)
    total_engagments = models.PositiveIntegerField(default=0)
    stream_growth = models.FloatField(default=0.0)
    updated_at = models.DateTimeField(auto_now=True)

class ChannelLink(models.Model):
    SPOTIFY = 'spotify'
    APPLE_MUSIC = 'apple_music'
    YOUTUBE = 'youtube' 
    INSTAGRAM = 'instagram'
    PLATFORM_CHOICES = [
        (SPOTIFY, 'Spotify'),
        (APPLE_MUSIC, 'Apple Music'),
        (YOUTUBE, 'YouTube'),
        (INSTAGRAM, 'Instagram'),
    ]

    artist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='channels')
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    url = models.URLField()
    is_connected = models.BooleanField(default=False)

class TrendAlert(models.Model):
    artist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trend_alerts')
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='trend_alerts')
    alert_type = models.CharField(max_length=50)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
        
    