from django.contrib import admin
#
from .models import Account, AccountType
# Register your models here.

class AccountAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'account_number',
        'owner',
        'type',
        'balance',
        'is_active',
    )

admin.site.register(Account, AccountAdmin)


class AccountTypeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'description',
    )

admin.site.register(AccountType, AccountTypeAdmin)