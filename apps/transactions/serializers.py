
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import (transaction, DatabaseError, IntegrityError)

# local
from apps.bank_profiles.models import Profile
from apps.transactions.models import Transaction, BankChargeRevenue
from .utils import send_transfer_notification


class GetFullNameForTransferSerializer(serializers.Serializer):

    account_no = serializers.CharField(max_length=15, help_text=_(
        "Recipient Account Number"), min_length=8, required=True)

    full_name = serializers.CharField(max_length=50, read_only=True)

    def validate(self, attrs):
        account_no = attrs.get('account_no', None)

        if account_no is None or len(account_no) < 8:
            raise ValueError("Account number cannot be empty and cannot be less than 8 digits")

        if not Profile.objects.filter(account_no=account_no).exists():
            raise ValidationError("Account number is either invalid or does not exist")

        profile = Profile.objects.get(account_no=account_no)

        return {
            'account_no': account_no,
            'full_name': profile.user.full_name
        }


class TransferSerializer(serializers.ModelSerializer):
    account_no = serializers.CharField(max_length=15, help_text=_(
        "Recipient Account Number"), min_length=8, required=True)
    amount = serializers.DecimalField(source="amount")
    description = serializers.CharField(source="description")

    class Meta:
        model = Transaction
        fields = ['account_no', "amount", 'description']

    def validate(self, attrs):
        account_no = attrs.get("account_no", None)
        amount = attrs.get("amount", None)
        request = self.context.get('request')
        user_profile = request.user.profile

        if account_no is None or len(account_no) < 8:
            raise ValueError("Account number cannot be empty and cannot be less than 8 digits")

        if not Profile.objects.filter(account_no=account_no).exists():
            raise ValidationError("Account number is either invalid or does not exist")

        if amount is None:
            raise ValueError("Amount field cannot be empty")

        if not amount.isdigit():
            raise ValidationError("Amount field is invalid")

        total = float(amount) + 0.80

        if user_profile.account_balance < total:
            raise ValidationError("Insufficient Balance")

        return super().validate(attrs)

    def save(self, request):
        sender = Profile.objects.get(user=request.user)
        amount = float(self.amount)
        charge = 1.25 if amount > 100 else 0.80
        description = self.description
        total = amount + charge
        receiver_profile = Profile.objects.get(account_no=self.account_no)

        try:
            transfer = Transaction.objects.create(sender=sender, to_account=self.account_no,
                                                  amount=total, description=description, charge=charge)
            with transaction.atomic():
                sender.account_balance - total
                receiver_profile.account_balance + amount
                transfer.is_completed = True
                transfer.save()

        except (DatabaseError, IntegrityError):
            transfer.is_completed = False
            send_transfer_notification(amount=amount, _from=sender, to=receiver_profile, is_successful=False)
        else:
            send_transfer_notification(amount=amount, _from=sender, to=receiver_profile, is_successful=True)
            BankChargeRevenue.objects.create(source=transfer, amount=charge)
