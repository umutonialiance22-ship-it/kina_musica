from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiExample
from .models import User, PasswordResetOTP
from .serializers import (UserSerializer, RegisterSerializer, LoginSerializer,
                           LogoutSerializer, RequestOTPSerializer,
                           VerifyOTPSerializer, ResetPasswordSerializer)
import random
from django.utils import timezone
from datetime import timedelta


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="Register a new user",
        description="Creates a new Vocalist or Artist account.",
        tags=['AUTH'],
        examples=[
            OpenApiExample(
                'Register Example',
                value={
                    'full_name': 'Amoni King',
                    'email': 'amoni@gmail.com',
                    'password': 'test1234',
                    'confirm_password': 'test1234',
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


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="Login",
        description="Login with role, email and password. Returns JWT tokens.",
        request=LoginSerializer,
        tags=['AUTH'],
        examples=[
            OpenApiExample(
                'Login Example',
                value={
                    'email': 'amoni@gmail.com',
                    'password': 'test1234',
                    'role': 'vocalist',
                }
            )
        ]
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        role = serializer.validated_data['role']

        try:
            user = User.objects.get(email=email)
            if not user.check_password(password):
                return Response({'error': 'Invalid credentials'}, status=400)

            # Update role to whatever the user selected at login
            user.role = role
            user.save(update_fields=['role'])

            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            })
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="Logout",
        description="Blacklists the refresh token to log the user out.",
        request=LogoutSerializer,
        tags=['AUTH'],
    )
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logged out successfully'})
        except Exception:
            return Response({'message': 'Logged out'})


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(summary="Get current user profile", tags=['AUTH'])
    def get_object(self):
        return self.request.user


class RequestOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="Request password reset OTP",
        description="Sends a 6-digit OTP to the user's email for password reset.",
        request=RequestOTPSerializer,
        tags=['AUTH'],
        examples=[
            OpenApiExample('OTP Request', value={'email': 'amoni@gmail.com'})
        ]
    )
    def post(self, request):
        email = request.data.get('email')
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


class VerifyOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="Verify OTP code",
        description="Verifies the 6-digit OTP sent to the user's email.",
        request=VerifyOTPSerializer,
        tags=['AUTH'],
        examples=[
            OpenApiExample(
                'OTP Verification',
                value={'email': 'amoni@gmail.com', 'otp_code': '123456'}
            )
        ]
    )
    def post(self, request):
        email = request.data.get('email')
        otp_code = request.data.get('otp_code')
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


class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="Reset password after OTP verification",
        description="Sets a new password after OTP has been verified.",
        request=ResetPasswordSerializer,
        tags=['AUTH'],
        examples=[
            OpenApiExample(
                'Reset Password',
                value={'user_id': 1, 'new_password': 'newpassword123'}
            )
        ]
    )
    def post(self, request):
        user_id = request.data.get('user_id')
        new_password = request.data.get('new_password')
        try:
            user = User.objects.get(id=user_id)
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password changed successfully'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)