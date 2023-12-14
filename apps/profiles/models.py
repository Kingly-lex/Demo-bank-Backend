from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField
from PIL import Image
from django_countries.fields import CountryField
from django.core.validators import MinLengthValidator
import random

# custom imports
from apps.common.models import HelperModel


User = get_user_model()


class Gender(models.TextChoices):
    MALE = "Male", _("Male")
    FEMALE = "Female", _("Female")
    OTHER = "Other", _("Other")


class Profile(HelperModel):

    user = models.OneToOneField(
        User, related_name="profile", on_delete=models.CASCADE)

    account_no = models.CharField(
        max_length=20, unique=True,
        editable=False, default='generate_account_no()')

    account_balance = models.DecimalField(
        decimal_places=2, max_digits=100, verbose_name=_("Account balance"), default=0.00)

    transfer_pin = models.IntegerField(
        validators=[MinLengthValidator(limit_value=4, message="Pin must be between 4 to 6 digits")], default=000000)

    phone_number = PhoneNumberField(
        verbose_name=_("Phone Number"), max_length=30, blank=True, null=True)

    profile_photo = models.ImageField(verbose_name=_("Profile Photo"),
                                      default="default.png", upload_to="profile_images")

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


def generate_account_no():
    num = str(random.randint(100000000, 999999999))

    if Profile.objects.get(account_no=num).exists():
        generate_account_no()
    else:
        return num
