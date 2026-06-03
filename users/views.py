from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema, OpenApiExample
from .models import User, PasswordResetOTP
from .serializers import (UserSerializer, RegisterSerializer, LoginSerializer, 
                          LogoutSerializer, RequestOTPSerializer, VerifyOTPSerializer, 
                          ResetPasswordSerializer, RequestOTPViewSerializer, VerifyOTPViewSerializer, 
                          ResetPasswordViewSerializer)
import random
from django.utils import timezone
from datetime import timedelta


@extend_schema(tags=['AUTH'])
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="Register a new user",
        description="Creates a new Fan or Artist account and returns JWT tokens.",
        tags=['AUTH'],
        examples=[
            OpenApiExample(
                'Fan Registration',
                value={
                    'username': 'johndoe',
                    'email': 'john@gmail.com',
                    'password': 'securepass123',
                    'role': 'fan'
                }
            ),
            OpenApiExample(
                'Artist Registration',
                value={
                    'username': 'artistking',
                    'email': 'artist@gmail.com',
                    'password': 'securepass123',
                    'role': 'artist'
                }
            ),
        ]
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=201)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="Login",
        description="Login with username and password. Returns JWT access and refresh tokens.",
        tags=['AUTH'],
        request=LoginSerializer,
        examples=[
            OpenApiExample(
                'Login Example',
                value={'username': 'johndoe', 'password': 'securepass123'}
            )
        ]
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            })
        return Response({'error': 'Invalid credentials'}, status=400)


class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="Logout",
        description="Blacklists the refresh token to log the user out.",
        tags=['AUTH'],
        request=LogoutSerializer,
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.validated_data.get('refresh')
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logged out successfully'})
        except Exception:
            return Response({'message': 'Logged out'})


@extend_schema(tags=['AUTH'])
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class RequestOTPView(generics.GenericAPIView):
    serializer_class = RequestOTPViewSerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="Request password reset OTP",
        description="Sends a 6-digit OTP to the user's email for password reset.",
        request=RequestOTPViewSerializer,
        tags=['AUTH'],
        examples=[
            OpenApiExample('OTP Request', value={'email': 'john@gmail.com'})
        ]
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        try:
            user = User.objects.get(email=email)
            otp_code = str(random.randint(100000, 999999))
            expires_at = timezone.now() + timedelta(minutes=10)
            PasswordResetOTP.objects.create(
                user=user,
                otp_code=otp_code,
                expires_at=expires_at
            )
            return Response({'message': 'OTP sent', 'otp': otp_code})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)


class VerifyOTPView(generics.GenericAPIView):
    serializer_class = VerifyOTPViewSerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="Verify OTP code",
        description="Verifies the 6-digit OTP sent to the user's email.",
        tags=['AUTH'],
        request=VerifyOTPViewSerializer,
        examples=[
            OpenApiExample(
                'OTP Verification',
                value={'email': 'john@gmail.com', 'otp_code': '123456'}
            )
        ]
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        otp_code = serializer.validated_data.get('otp_code')
        try:
            user = User.objects.get(email=email)
            otp = PasswordResetOTP.objects.filter(
                user=user,
                otp_code=otp_code,
                is_used=False,
                expires_at__gt=timezone.now()
            ).latest('created_at')
            otp.is_used = True
            otp.save()
            return Response({'message': 'OTP verified', 'user_id': user.id})
        except (User.DoesNotExist, PasswordResetOTP.DoesNotExist):
            return Response({'error': 'Invalid or expired OTP'}, status=400)


class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordViewSerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="Reset password",
        description="Sets a new password after OTP verification.",
        tags=['AUTH'],
        request=ResetPasswordViewSerializer,
        examples=[
            OpenApiExample(
                'Reset Password',
                value={'user_id': 1, 'new_password': 'newpassword123'}
            )
        ]
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = serializer.validated_data.get('user_id')
        new_password = serializer.validated_data.get('new_password')
        try:
            user = User.objects.get(id=user_id)
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password changed successfully'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)
