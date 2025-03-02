from rest_framework import generics, status, permissions, serializers
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from .utils import send_otp_email
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


User = get_user_model()

class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)  # Call the default create method
        user = User.objects.get(id=response.data['id'])

        # Generate and send OTP
        user.generate_otp()
        send_otp_email(user)

        return Response(
            {"message": "User registered successfully. Please verify your email with the OTP sent."},
            status=status.HTTP_201_CREATED
        )



class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        otp_code = request.data.get("otp")  # Match frontend request

        try:
            user = User.objects.get(email=email)

            print(f"Received OTP: {otp_code}, Stored OTP: {user.otp_code}")  # Debugging

            if user.otp_code == otp_code:
                user.is_verified = True
                user.otp_code = None  # Clear OTP after verification
                user.save()
                return Response({"message": "Account verified successfully!"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Ensure user exists before checking verification status
        if not hasattr(self, 'user') or not self.user.is_verified:
            raise serializers.ValidationError("Your account is not verified. Please verify your email with the OTP sent.")

        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
