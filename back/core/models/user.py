from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from .base import TimestampedModel
from .language import Language

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50, blank=True)
    langauge = models.ForeignKey(
        Language, 
        to_field="language_code", 
        null=True, blank=True, 
        on_delete=models.SET_NULL
    )
    language_code = models.CharField(max_length=10, blank=True, null=True)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    conversations_quota = models.IntegerField(default=10)  
    conversations_count = models.IntegerField(default=0)
    last_summary_generated = models.BooleanField(default=False, blank=False)
    last_analysis_summary_en = models.TextField(blank=True, default='')
    last_analysis_summary_ar = models.TextField(blank=True, default='')
    last_analysis_date = models.DateTimeField(null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    username = None

    def __str__(self):
        return self.email
