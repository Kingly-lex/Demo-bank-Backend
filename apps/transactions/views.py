from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView, ListAPIView
from django.db.models import Q

# local
from .serializers import TransferSerializer, GetFullNameForTransferSerializer, TransactionHistorySerializer
from .models import Transaction
from apps.bank_profiles.models import Profile


class GetFullNameForTransfer(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GetFullNameForTransferSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransferView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TransferSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            serializer.save(attrs=serializer.data, request=request)
            return Response({'response': "Transfer was successful"}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionHistory(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionHistorySerializer

    def name(self, acct):
        profile = Profile.objects.get(account_no=acct)
        return profile.user.full_name

    def get_queryset(self):
        profile = self.request.user.profile
        query_set = Transaction.objects.filter(Q(sender=profile.account_no) |
                                               Q(receiver=profile.account_no)
                                               ).order_by('-created_at').all()

        for obj in query_set:
            obj.sender = "Self" if profile.account_no == obj.sender else self.name(acct=obj.sender)
            obj.receiver = 'Self' if profile.account_no == obj.receiver else self.name(acct=obj.receiver)
            obj.created_at = obj.created_at.strftime('%B %d, %Y %I:%M:%S %p')

        return query_set
