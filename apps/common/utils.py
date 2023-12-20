import random
from celery import shared_task
from apps.common.models import AllAcountNumbers


@shared_task(bind=True)
def test_function(self):
    pass


def generate_account_no() -> str:
    num = str(random.randint(100000000, 99999999999))
    if AllAcountNumbers.objects.filter(account_no=num).exists():
        generate_account_no()
    prefix = '51'
    return prefix + num
