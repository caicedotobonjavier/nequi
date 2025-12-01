from django.db import models
#
from model_utils.models import TimeStampedModel
#
from django.conf import settings
# Create your models here.

class AccountType(TimeStampedModel):

    TYPE_ACCOUNT = (
        ('0', 'Cuenta Ahorros'),
        ('1', 'Cuenta Corriente'),
        ('2', 'CDT'),
        ('3', 'Tarjeta Credito'),
    )

    name = models.CharField('Type Account', max_length=1, choices=TYPE_ACCOUNT)
    description = models.CharField('Description', max_length=255)


    class Meta:
        verbose_name = 'Account_Type'
        verbose_name_plural = 'Account_Types'
        ordering = ['id']
    

    def __str__(self):
        return self.name



class Account(TimeStampedModel):
    account_number = models.CharField('Account Number', max_length=20, unique=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='accounts')
    type = models.ForeignKey(AccountType, on_delete=models.PROTECT)
    balance = models.PositiveIntegerField('Balance', default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'
        ordering = ['account_number']
    

    def __str__(self):
        return self.account_number