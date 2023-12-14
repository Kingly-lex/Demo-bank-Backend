import random
from .models import Profile


def generate_account_no():
    num = str(random.randint(100000000, 999999999))

    if Profile.objects.get(account_no=num).exists():
        generate_account_no()
    else:
        return num


def send_verify_email():
    pass
