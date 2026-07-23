from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    VOCALIST = 'vocalist'
    ARTIST = 'artist'
    ROLE_CHOICES = [
        (VOCALIST, 'Vocalist'),
        (ARTIST, 'Artist'),
    ]

    GOOGLE = 'google'
    PHONE = 'phone'
    EMAIL = 'email'
    AUTH_CHOICES = [
        (GOOGLE, 'Google'),
        (PHONE, 'Phone'),
        (EMAIL, 'Email'),
    ]

    KINYARWANDA = 'rw'
    SWAHILI = 'sw'
    ENGLISH = 'en'
    FRENCH = 'fr'
    LANGUAGE_CHOICES = [
        (KINYARWANDA, 'Kinyarwanda'),
        (SWAHILI, 'Swahili'),
        (ENGLISH, 'English'),
        (FRENCH, 'French'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=VOCALIST)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default=ENGLISH)
    auth_provider = models.CharField(max_length=10, choices=AUTH_CHOICES, default=EMAIL)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    # ✅ ADD THESE THREE LINES — lets Django use email as the login field
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

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