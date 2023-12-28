from django.core.mail import EmailMessage
from django.conf import settings


def send_transfer_credit_notification(amount, sender, receiver, desc, datetime):
    msg = f"Hi {receiver.user.full_name},\n{sender.user.full_name} just sent you ${amount}\nDescription: {desc}"
    balance = receiver.account_balance
    mail = EmailMessage(
        body=msg + f"\nBalance: {balance}\nDate: {datetime.strftime('%B %d, %Y %I:%M:%S %p')}",
        to=[sender.user.email],
        subject='Credit Alert',
        from_email=settings.DEFAULT_FROM_EMAIL,
    )
    mail.send(fail_silently=True)


def send_transfer_debit_notification(amount, charge, sender, receiver, desc, datetime):
    msg = f"Hi {sender.user.full_name},\nYou just sent ${amount}, to {receiver.user.full_name}\nDescription: {desc}"
    balance = sender.account_balance
    mail = EmailMessage(
        body=msg + f"\nCharge: ${charge}\nBalance: {balance}\nDate: {datetime.strftime('%B %d, %Y %I:%M:%S %p')}",
        to=[receiver.user.email],
        subject='Debit Alert',
        from_email=settings.DEFAULT_FROM_EMAIL,
    )
    mail.send(fail_silently=True)
