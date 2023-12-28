from django.db import models
from django.utils.translation import gettext_lazy as _

# local
from apps.common.models import HelperModel
from apps.bank_profiles.models import Profile


class Type(models.TextChoices):
    Transfer = "Transfer", _("Transfer")
    Withdrawal = "Withdrawal", _("Withdrawal")
    Deposit = "Deposit", _("Deposit")


class Transaction(HelperModel):
    sender = models.TextField(max_length=20, verbose_name=_("Sender Account Number"))

    receiver = models.TextField(max_length=20, verbose_name=_("Receiver Account Number"))

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    type = models.TextField(max_length=20, choices=Type.choices, default=Type.Transfer)

    processed_by = models.TextField(max_length=100, verbose_name=_("Banker id"), default='Auto-transfer')

    charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    description = models.TextField(max_length=200, blank=True, null=True)

    is_successful = models.BooleanField(default=False)

    def __str__(self) -> str:
        r_profile = Profile.objects.get(account_no=self.receiver)
        date = self.created_at.strftime('%B %d, %Y %I:%M:%S %p')
        return f"Type: {self.type}, Destination:{r_profile.user.full_name} Amount: ${self.amount} on {date}"
