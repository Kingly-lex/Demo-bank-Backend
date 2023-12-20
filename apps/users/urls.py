from django.urls import path

# custom imports
from .views import (RegisterView, LoginView, LogoutView, Request_new_verification_email,
                    ActivateAccount, ChangePassword, SetNewPassword, PasswordResetConfirmWeb, ForgotPassword)


urlpatterns = [
    path('auth/register', RegisterView.as_view(), name='register'),

    path('auth/activate', ActivateAccount.as_view(), name='activate'),

    path('auth/login', LoginView.as_view(), name='login'),

    path('auth/change_password', ChangePassword.as_view(), name='change_password'),

    path('auth/logout', LogoutView.as_view(), name='logout'),

    path('auth/request_new_verification_email',
         Request_new_verification_email.as_view(), name='request_new_verification_email'),

    path('auth/forgot_password', ForgotPassword.as_view(), name='forgot_password'),

    path('auth/reset_confirm/<uidb64>/<token>', PasswordResetConfirmWeb.as_view(), name='reset_confirm'),

    path('auth/set_password', SetNewPassword.as_view(),
         name='set_password'),
]
