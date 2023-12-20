from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
import uuid
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from PIL import Image
from django_countries.fields import CountryField
from django.core.validators import MinLengthValidator

# from werkzeug.security import generate_password_hash


# custom imports
from apps.common.models import HelperModel
from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(max_length=100, unique=True, verbose_name=_("Email Address"))
    username = models.CharField(verbose_name=_("Username"), max_length=50, unique=True)
    first_name = models.CharField(verbose_name=_("First Name"), max_length=50)
    last_name = models.CharField(verbose_name=_("Last Name"), max_length=50)
    middle_name = models.CharField(verbose_name=_("Middle Name"), max_length=50, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
        "first_name",
        "last_name",
    ]

    objects = CustomUserManager()

    @property
    def full_name(self):

        if self.middle_name is not None and self.middle_name != '':
            return f"{self.first_name} {self.middle_name} {self.last_name}"

        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.username

#
#


class OTPForUser(models.Model):
    user = models.ForeignKey(User, related_name='otp', on_delete=models.CASCADE)
    email_otp = models.CharField(max_length=6, null=True, blank=True)


class Gender(models.TextChoices):
    MALE = "Male", _("Male")
    FEMALE = "Female", _("Female")
    OTHER = "Other", _("Other")


class VerificationMethod(models.TextChoices):
    NIN = "NIN", _("NIN")
    DRIVING_LICENCE = "DRIVING_LICENCE", _("DRIVING_LICENCE")
    PASSPORT = "PASSPORT", _("PASSPORT")


class Profile(HelperModel):

    user = models.OneToOneField(
        User, related_name="profile", on_delete=models.CASCADE)

    account_no = models.CharField(
        max_length=20, unique=True, null=True, blank=True)

    account_balance = models.DecimalField(
        decimal_places=2, max_digits=100, verbose_name=_("Account balance"), default=0.00)

    transfer_pin = models.CharField(
        validators=[MinLengthValidator(4)], default=123456)

    phone_number = PhoneNumberField(
        verbose_name=_("Phone Number"), help_text=_("Eg: +234758849930"), max_length=30, blank=True, null=True)

    profile_photo = models.ImageField(verbose_name=_("Profile Photo"),
                                      default="default.jpg", upload_to="profile_images")

    verification_method = models.CharField(choices=VerificationMethod.choices,
                                           default=VerificationMethod.NIN, max_length=50)

    Verification_id = models.ImageField(verbose_name=_("Verification_id"),
                                        upload_to="Verification_images", blank=True, null=True)

    gender = models.CharField(choices=Gender.choices,
                              default=Gender.OTHER, max_length=10)

    country = CountryField(
        verbose_name=_("Country"), default="NG")

    city = models.CharField(
        verbose_name=_("City"),
        max_length=100,
        default=''
    )

    address = models.TextField(max_length=255, verbose_name=_("Your Address"),
                               blank=True, null=True,)

    def __str__(self):
        return f"{self.user}'s Profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.profile_photo.path)

        if img.height > 300 or img.width > 300:
            img_dimensions = (300, 300)
            img.thumbnail(img_dimensions)
            img.save(self.profile_photo.path)

        # # pin secure
        # self.transfer_pin = generate_password_hash(self.transfer_pin, method="pbkdf2:sha256", salt_length=16)
