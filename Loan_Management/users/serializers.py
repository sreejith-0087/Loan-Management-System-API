from rest_framework import serializers
from django.core.mail import send_mail
import random
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)  # Hash password
        user.is_verified = False  # Ensure user is unverified at start

        # Generate and assign OTP
        user.otp_code = str(random.randint(100000, 999999))
        user.save()

        # Send OTP email
        send_mail(
            subject="Verify Your Account",
            message=f"Your OTP code is {user.otp_code}",
            from_email="noreply@example.com",
            recipient_list=[user.email],
            fail_silently=False,
        )

        return user
