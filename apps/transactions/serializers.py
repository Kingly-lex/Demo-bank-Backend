
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import transaction
import decimal
# from django.db.models import Q

# local imports
from apps.bank_profiles.models import Profile
from apps.transactions.models import Transaction
from .utils import send_transfer_credit_notification, send_transfer_debit_notification


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
    account_no = serializers.CharField(max_length=15, help_text=_("Recipient Account"), min_length=8, required=True)
    description = serializers.CharField(max_length=200)
    charge = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Transaction

        fields = [
            'account_no',
            'amount',
            'description',
            'charge']

    def validate(self, attrs):
        account_no = attrs.get("account_no", None)
        description = attrs.get("description", None)
        amount = decimal.Decimal(attrs.get("amount", None))
        request = self.context.get('request')
        charge = decimal.Decimal(1.25 if amount > 100 else 0.80)
        user_profile = request.user.profile

        if account_no is None or len(account_no) < 8:
            raise ValueError("Account number cannot be empty and cannot be less than 8 digits")

        if not Profile.objects.filter(account_no=account_no).exists():
            raise ValidationError("Account number is either invalid or does not exist")

        if amount is None:
            raise ValueError("Amount field cannot be empty")

        if not user_profile.is_updated:
            raise ValidationError("You are not eligible for transfers")

        total = amount + charge

        if user_profile.account_balance < total:
            raise ValidationError("Insufficient Balance")

        return {
            "account_no": account_no,
            "amount": amount,
            "description": description,
            "charge": charge
        }

    def save(self, attrs, request):
        sender_profile = Profile.objects.get(user=request.user)
        amount = decimal.Decimal(attrs.get('amount'))
        charge = decimal.Decimal(attrs.get('charge'))
        description = attrs.get('description')
        total = amount + charge
        receiver_profile = Profile.objects.get(account_no=attrs.get('account_no'))

        with transaction.atomic():
            transfer = Transaction.objects.create(sender=sender_profile.account_no, receiver=attrs.get('account_no'),
                                                  amount=total, description=description, charge=charge)

            sender_profile.account_balance -= total
            receiver_profile.account_balance += amount
            transfer.is_successful = True
            transfer.save()
            sender_profile.save()
            receiver_profile.save()

        send_transfer_credit_notification(amount=amount, sender=sender_profile,
                                          receiver=receiver_profile, desc=description, datetime=transfer.created_at)

        send_transfer_debit_notification(amount=amount, sender=sender_profile, receiver=receiver_profile,
                                         desc=description, datetime=transfer.created_at, charge=charge)


class TransactionHistorySerializer(serializers.ModelSerializer):
    reference_id = serializers.CharField(source='id', read_only=True)
    date = serializers.CharField(source='created_at', read_only=True)

    class Meta:
        model = Transaction

        fields = [
            'reference_id',
            'sender',
            'receiver',
            'amount',
            'type',
            'charge',
            'description',
            'processed_by',
            'is_successful',
            'date'
        ]

        read_only_fields = [
            'reference_id',
            'sender',
            'receiver',
            'type',
            'amount',
            'charge',
            'description',
            'processed_by',
            'is_successful',
            'date'
        ]
