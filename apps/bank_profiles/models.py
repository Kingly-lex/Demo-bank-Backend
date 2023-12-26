from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from PIL import Image
from django_countries.fields import CountryField
from django.core.validators import MinLengthValidator

# from werkzeug.security import generate_password_hash


# custom imports
from apps.common.models import HelperModel
from apps.users.models import User


class AcountNumbers(HelperModel):
    account_no = models.TextField(max_length=50, unique=True, null=True, blank=True)

    def __str__(self):
        return self.account_no

    class Meta:
        verbose_name_plural = 'AccountNumbers'


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

    account_no = models.TextField(max_length=20, unique=True, null=True, blank=True)

    account_balance = models.DecimalField(decimal_places=2, max_digits=100,
                                          verbose_name=_("Account balance"), default=0.00)

    transfer_pin = models.TextField(validators=[MinLengthValidator(4)], max_length=4, default='1234')

    phone_number = PhoneNumberField(
        verbose_name=_("Phone Number"), region='NG', help_text=_("Eg: +234758849930"), max_length=30, null=True)

    profile_photo = models.ImageField(verbose_name=_("Profile Photo"),
                                      default="default.jpg", upload_to="profile_images")

    verification_method = models.TextField(choices=VerificationMethod.choices, default=VerificationMethod.NIN,
                                           help_text=_("NIN, DRIVING_LICENCE, PASSPORT"), max_length=50)

    Verification_id = models.ImageField(verbose_name=_("Verification_id"), upload_to="Verification_images", null=True)

    gender = models.TextField(choices=Gender.choices, default=Gender.OTHER, max_length=10)

    country = CountryField(verbose_name=_("Country"), default="NG")

    city = models.TextField(verbose_name=_("City"), max_length=100, null=True)

    address = models.TextField(max_length=255, verbose_name=_("Your Address"), null=True)

    is_updated = models.BooleanField(default=False)

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
