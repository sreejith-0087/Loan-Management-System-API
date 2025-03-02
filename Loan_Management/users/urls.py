from django.urls import path
from .views import RegisterUserView, VerifyOTPView, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # ✅ FIXED HERE
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
