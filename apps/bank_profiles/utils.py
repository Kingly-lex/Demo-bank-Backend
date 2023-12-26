import random
from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings

# local
from .models import AcountNumbers


@shared_task(bind=True)
def test_function(self):
    pass


def generate_account_no():
    num = '51' + str(random.randint(1000000, 9999999))
    if AcountNumbers.objects.filter(account_no=num).exists():
        generate_account_no()
    AcountNumbers.objects.create(account_no=num)
    return num


def send_update_profile_email(email):
    mail = EmailMessage(subject="Update your Profile",
                        body="""Now that your email has been verified,\n
Please update your profile information to get started with our banking services""",
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[email])
    mail.send(fail_silently=True)


def send_account_number_notification(email, acct_no):
    mail = EmailMessage(subject="Your account number is ready",
                        body=f"Your account number is {acct_no}, You can now send or receive funds, Hooray!",
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[email])
    mail.send(fail_silently=True)
