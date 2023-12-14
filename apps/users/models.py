from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
import uuid
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


# custom imports
from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(max_length=100, unique=True, editable=False, verbose_name=_("Email Address"))
    username = models.CharField(verbose_name=_("Username"), max_length=50, unique=True)
    first_name = models.CharField(verbose_name=_("First Name"), max_length=50)
    last_name = models.CharField(verbose_name=_("Last Name"), max_length=50)
    middle_name = models.CharField(verbose_name=_("Middle Name"), max_length=50, default=None)

    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
        "first_name",
        "last_name",
    ]

    objects = CustomUserManager()

    @property
    def full_name(self):

        if self.middle_name is not None:
            return f"{self.first_name} {self.middle_name} {self.last_name}"

        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.username


class OTP(models.Model):
    user = models.OneToOneField(
        User, related_name='otp', on_delete=models.CASCADE)

    code = models.CharField(max_length=6)

    def __str__(self):
        return f"{self.user.username} - OTP"
