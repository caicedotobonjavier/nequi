from django.contrib import admin
#
from .models import Transaction
# Register your models here.

class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'transaction_type',
        'account',
        'amount',
        'balance_after',
        'timestamp',
        'description',
        'target_account',
    )

admin.site.register(Transaction, TransactionAdmin)