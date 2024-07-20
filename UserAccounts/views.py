from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from .models import CustomUser, OTP
from .serializers import UserRegistrationSerializer, OTPVerificationSerializer
import random

class RegisterUser(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        otp = ''.join(random.choices('0123456789', k=6))
        OTP.objects.create(email=email, otp=otp)

        # Send OTP to the user's email
        send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp}',
            'from@example.com',  # Replace with your email
            [email],
            fail_silently=False,
        )

        return Response({"message": "OTP sent"}, status=status.HTTP_200_OK)

class VerifyOTP(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        password = request.data.get('password')
        if not email or not otp or not password:
            return Response({"error": "Email, OTP, and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            otp_record = OTP.objects.get(email=email, otp=otp)
        except OTP.DoesNotExist:
            return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.create_user(email=email, password=password)
        otp_record.delete()
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
