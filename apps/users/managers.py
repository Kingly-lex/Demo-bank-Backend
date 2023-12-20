from django.contrib.auth.models import BaseUserManager
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def email_validator(self, email):
        try:
            email = self.normalize_email(email)
            validate_email(email)
        except ValidationError:
            ValueError("Email address is not valid")

    def create_user(self, email, username, first_name, last_name, password, **extra_fields):
        if not email:
            raise ValueError(_("Users must have an email address"))

        if not username:
            raise ValueError(_("Users must submit a username"))

        if not first_name:
            raise ValueError(_("Users must submit a first name"))

        if not last_name:
            raise ValueError(_("Users must submit a last name"))

        middle_name = extra_fields.get("middle_name", '')

        self.email_validator(email)

        user = self.model(email=email, username=username, middle_name=middle_name,
                          first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, password):

        user = self.create_user(email, username, first_name, last_name, password)

        user.is_admin = True
        user.is_verified = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.is_superuser = True

        user.save(using=self._db)
        return user
