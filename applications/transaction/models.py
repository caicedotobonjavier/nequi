from django.db import models
#
from model_utils.models import TimeStampedModel
#
from applications.users.models import User
#
from applications.account.models import Account
#

# Create your models here.

class Transaction(TimeStampedModel):

    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"
    TRANSFER = "TRANSFER"

    TRANSACTION_TYPES = (
        (DEPOSIT, 'Consignacion'),
        (WITHDRAW, 'Retiro'),
        (TRANSFER, 'Transferencia'),
    )

    transaction_type = models.CharField('Transaction Type', max_length=15, choices=TRANSACTION_TYPES)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    amount = models.PositiveIntegerField('Amount')
    balance_after = models.PositiveIntegerField('Balance After')
    timestamp = models.DateTimeField('Time Stamp', auto_now_add=True)
    description = models.TextField('Description', blank=True, null=True)
    target_account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='incoming_transfer',
        null=True,
        blank=True
    )


    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ["-timestamp"]
    

    def __str__(self):
        return f'{self.transaction_type} - {self.amount} - {self.timestamp}'