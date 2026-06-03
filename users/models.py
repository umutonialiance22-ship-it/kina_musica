from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


# Create your models here.
class User(AbstractUser):
    FAN = 'fan'
    ARTIST = 'artist'
    ROLE_CHOICES = [
        (FAN, 'Fan'),
        (ARTIST, 'Artist'),
    ]
    GOOGLE = 'GOOGLE'
    PHONE = 'PHONE'
    EMAIL = 'EMAIL'

    AUTH_CHOICES = [
        (GOOGLE, 'GOOGLE'),
        (PHONE, 'PHONE'),
        (EMAIL, 'EMAIL'),
    ]


    KINYARWANDA = 'rw'
    SWAHILI = 'sw'
    ENGLISH = 'en'
    FRENCH = 'fr'
    LANGUAGE_CHOICES = [
        (KINYARWANDA, 'KINYARWANDA'),
        (SWAHILI, 'SWAHILI'),
        (ENGLISH, 'ENGLISH'),
        (FRENCH, 'FRENCH'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=FAN)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default=ENGLISH)
    auth_provider = models.CharField(max_length=10, choices=AUTH_CHOICES, default=EMAIL)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"
    
class PasswordResetOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otps')
    otp_code = models.CharField(max_length=6)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OTP for {self.user.username}"

class PayoutDetail(models.Model):
    artist = models.OneToOneField(User, on_delete=models.CASCADE, related_name='payout')
    bank_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=50)
    account_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payout for {self.artist.username}"        
