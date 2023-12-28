from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from apps.bank_profiles.models import Profile as P, NextOfKin as K


User = get_user_model()


class UserAdmin(DefaultUserAdmin):
    list_display_links = ['id', 'email', 'first_name', 'last_name', "username",]
    list_display = ['pkid', 'id', 'email', "username", 'first_name', 'last_name', "is_staff", "is_active"]
    list_filter = ['email', "username", 'first_name', 'last_name', "is_staff", "is_active"]
    filter_horizontal = ()
    model = User
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    fieldsets = (
        (
            _("Login Credentials"),
            {
                "fields": (
                    "email",
                    "password",
                )
            },
        ),
        (
            _("Personal Information"),
            {
                "fields": (
                    "username",
                    "first_name",
                    "last_name",
                    'middle_name',
                )
            },
        ),
        (
            _("Permissions and Groups"),
            {
                "fields": (
                    "is_active",
                    "is_verified",
                    "is_staff",
                    "is_admin",
                    "is_superadmin",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important Dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "is_staff", "is_active"),
            },
        ),
    )
    search_fields = ["email", "username", "first_name", "last_name"]


class Profile(P):
    class Meta:
        proxy = True


class NextOfKin(K):
    class Meta:
        proxy = True


admin.site.register(User, UserAdmin)
admin.site.register(Profile)
admin.site.register(NextOfKin)
