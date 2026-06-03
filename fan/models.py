from django.db import models
from users.models import User
from songs.models import Song

# Create your models here.
class Favorite(models.Model):
    fan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='favorited_by')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('fan', 'song')

class History(models.Model):
    fan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='history')
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='played_by')
    played_at = models.DateTimeField(auto_now_add=True)

class Recording(models.Model):
    fan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recordings')
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='recorded_by')
    audio_url = models.FileField(upload_to='recordings/')
    recorded_at = models.DateTimeField(auto_now_add=True)

class Follower(models.Model):
    fan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    artist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    followed_at = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)
    class Meta:
        unique_together = ('fan', 'artist')

class Comment(models.Model):
    fan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    commented_at = models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    fan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='reviews_received')
    rating = models.PositiveIntegerField()
    content = models.TextField(null=True, blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)    

    class Meta:
        unique_together = ('fan', 'song')    

    
