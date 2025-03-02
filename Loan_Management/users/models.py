from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
import random



class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, username, password, **extra_fields)

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)  # OTP verification flag
    otp_code = models.CharField(max_length=6, blank=True, null=True)  # OTP field

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()  # Custom manager

    def generate_otp(self):
        """Generates and saves a 6-digit OTP."""
        self.otp_code = str(random.randint(100000, 999999))
        self.save()

