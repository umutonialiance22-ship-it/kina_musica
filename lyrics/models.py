from django.db import models
from songs.models import Song


# Create your models here.
class Lyric(models.Model):
    ARTIST = 'artist'
    API = 'api'
    SOURCE_CHOICES = [(ARTIST, 'Artist'), (API, 'API')]

    song = models.OneToOneField(Song, on_delete=models.CASCADE, related_name='lyric')
    plain_lyrics = models.TextField(null=True, blank=True)
    synced_Lrc = models.TextField(null=True, blank=True)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default=ARTIST)
    is_enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"Lyric for {self.song.title}" 
    

