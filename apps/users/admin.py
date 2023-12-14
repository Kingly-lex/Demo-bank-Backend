from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

# custom imports
# from .forms import UserChangeForm, MyUserChangeForm


User = get_user_model()


class UserAdmin(UserAdmin):
    list_display_links = ['email', 'id']
    # forms = UserChangeForm
    # add_form = MyUserChangeForm
    model = User
    list_display = [
        'pkid',
        'id',
        'email',
        'first_name',
        'last_name',
        "is_staff",
        "is_active",
    ]
    list_filter = [
        'email',
        "username",
        'first_name',
        'last_name',
        "is_staff",
        "is_active",
    ]


admin.site.register(User, UserAdmin)
# admin.site.register(User)
