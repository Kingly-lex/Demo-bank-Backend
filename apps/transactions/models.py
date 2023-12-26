from django.db import models
from django.utils.translation import gettext_lazy as _

# local
from apps.common.models import HelperModel
from apps.bank_profiles.models import Profile
from apps.users.models import User


class TransferType(models.TextChoices):
    TRANSFER = "Transfer", _("Transfer")
    WITHDRAWAL = "Withdrawal", _("Withdrawal")
    DEPOSIT = "Deposit", _("Deposit")


class Transaction(HelperModel):
    sender = models.ForeignKey(Profile, related_name="outgoing", on_delete=models.DO_NOTHING, null=True, blank=True)

    to_account = models.TextField(max_length=20, verbose_name=_("Receiver Account Number"))

    type = models.CharField(max_length=20, choices=TransferType.choices, default=TransferType.TRANSFER)

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.80)

    processed_by = models.ForeignKey(User, related_name='banker', help_text=_(
        "Staff who proccessed Withdrawal or deposit"), on_delete=models.DO_NOTHING, null=True, blank=True)

    description = models.TextField(max_length=200, blank=True, null=True)

    is_completed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.type}, Amount: ${self.amount} on {self.created_at.strftime('%B %d, %Y')}"


class BankChargeRevenue(HelperModel):
    source = models.ForeignKey(Transaction, related_name="bank_revenue", on_delete=models.DO_NOTHING)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
