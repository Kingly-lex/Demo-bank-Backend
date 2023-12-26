from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import Transaction


class TransactionAdmin(DefaultUserAdmin):
    list_display_links = ['id', 'type', 'amount', 'is_completed', 'created_at']
    list_display = ['id', 'type', 'amount', 'is_completed', 'created_at']
    list_filter = ['id', 'type', 'amount', 'is_completed', 'created_at']
    filter_horizontal = ()
    model = Transaction
    ordering = ['-created_at']


admin.site.register(Transaction, TransactionAdmin)
