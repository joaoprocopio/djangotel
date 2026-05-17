from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone


# https://docs.djangoproject.com/en/6.0/topics/auth/customizing/
class Conta(AbstractBaseUser, PermissionsMixin):
    display_name = models.CharField(max_length=320)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
