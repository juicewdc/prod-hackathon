from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager


class ProjectUser(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    username = models.CharField(max_length=50, null=True)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    def __str__(self):
        return self.email


