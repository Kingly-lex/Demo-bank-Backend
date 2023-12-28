from django.urls import path

from .views import TransferView, GetFullNameForTransfer, TransactionHistory

urlpatterns = [
    path('get_recipient', GetFullNameForTransfer.as_view(), name='get_recipient'),
    path('send', TransferView.as_view(), name='send'),
    path('history', TransactionHistory.as_view(), name='history'),
]
