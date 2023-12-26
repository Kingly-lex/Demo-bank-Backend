from django.urls import path

# custom imports
from .views import (RegisterView, LoginView, LogoutView, Request_new_verification_email,
                    ActivateAccount, ChangePassword, SetNewPassword, PasswordResetConfirmWeb, ForgotPassword)


urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),

    path('activate', ActivateAccount.as_view(), name='activate'),

    path('login', LoginView.as_view(), name='login'),

    path('change_password', ChangePassword.as_view(), name='change_password'),

    path('logout', LogoutView.as_view(), name='logout'),

    path('request_new_verification_email',
         Request_new_verification_email.as_view(), name='request_new_verification_email'),

    path('forgot_password', ForgotPassword.as_view(), name='forgot_password'),

    path('reset_confirm/<uidb64>/<token>', PasswordResetConfirmWeb.as_view(), name='reset_confirm'),

    path('set_password', SetNewPassword.as_view(),
         name='set_password'),
]
