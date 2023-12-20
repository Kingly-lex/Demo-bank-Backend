from rest_framework import serializers
from .models import AllAcountNumbers
from .utils import generate_account_no


class AccountGenerateSerializer(serializers.Serializer):
    account_no = serializers.CharField(max_length=100, read_only=True)

    class Meta:
        model = AllAcountNumbers
        fields = ['account_no']

    def get_account_no():
        code = generate_account_no()
        return {'account_no': code}
