from django.core.mail import EmailMessage
from django.conf import settings
import random
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site


# custom
from .models import OTPForUser, User


def create_jwt_pair_for_user(user: User):
    refresh = RefreshToken.for_user(user)

    tokens = {
        "access_token": str(refresh.access_token),
        "refresh_token": str(refresh),
    }

    return tokens


def send_verify_email_otp(email):
    user = User.objects.get(email=email)
    otp = random.randint(100000, 999999)

    OTPForUser.objects.create(user=user, email_otp=otp)

    email = email
    body = f"Hi {user.full_name}, \nThank you for registering with us, Please use {otp} to verify your account"

    mail = EmailMessage(from_email=settings.DEFAULT_FROM_EMAIL,
                        subject="Verify Your Email",
                        body=body,
                        to=[email]
                        )
    mail.send(fail_silently=True)


def send_password_reset_otp(email, request):
    current_site = get_current_site(request).domain
    user = User.objects.get(email=email)

    uidb64 = urlsafe_base64_encode(force_bytes(user.id))
    token = default_token_generator.make_token(user)
    url = reverse('reset_confirm', kwargs={'uidb64': uidb64, 'token': token})
    api_url = reverse('set_password')
    link = f"{current_site}{url}"
    msg_body = f"""Dear {user.full_name},\nYou have requested password reset, please visit {link}\nor\nuse uibd64:{uidb64} and token:{token} on {api_url}"""

    mail = EmailMessage(body=msg_body,
                        subject="Reset Your Password",
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[email]
                        )
    mail.send(fail_silently=True)
