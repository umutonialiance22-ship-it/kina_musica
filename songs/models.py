from django.db import models
from users.models import User
from albums.models import Album


# Create your models here.
class Song(models.Model):
    EASY = 'easy'
    MEDIUM = 'medium'
    HARD = 'hard'
    DIFFICULTY_CHOICES = [
        (EASY, 'Easy'),
        (MEDIUM, 'Medium'),
        (HARD, 'Hard'),
    ]

    artist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='songs')
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='songs', null=True, blank=True)
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=100, null=True, blank=True)
    era = models.CharField(max_length=100, null=True, blank=True)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default=EASY)
    audio_url = models.FileField(upload_to='songs/', null=True, blank=True)
    cover_image_url = models.ImageField (upload_to='song_covers/', null=True, blank=True)
    is_live = models.BooleanField(default=False)
    total_streams = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


