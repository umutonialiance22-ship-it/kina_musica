from django.db import models
from users.models import User

# Create your models here.
class Album(models.Model):
    artist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='albums')
    title = models.CharField(max_length=255)
    cover_image = models.ImageField(upload_to='albums/', null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    era = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
