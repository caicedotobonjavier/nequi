from django.db import transaction, IntegrityError
#
from .models import Transaction
#
from applications.account.models import Account
#


def service_deposit(account, amount, transaction_deposit, description):
    with transaction.atomic():
        account_transaction = Account.objects.select_for_update().get(account_number=account)
        balance_actualy = account_transaction.balance
        account_transaction.balance += amount
        account_transaction.save()

        transaction_execute = Transaction.objects.create(
            transaction_type = transaction_deposit,
            account = account_transaction,
            amount = amount,
            balance_after = balance_actualy,
            description = description
        )          
    
    return transaction_execute



def service_withdraw(account, amount, transaction_withdraw, description):
    with transaction.atomic():
        account_transaction = Account.objects.select_for_update().get(account_number=account)
        balance_actualy = account_transaction.balance
        account_transaction.balance -= amount
        account_transaction.save()

        transaction_execute = Transaction.objects.create(
            transaction_type = transaction_withdraw,
            account = account_transaction,
            amount = amount,
            balance_after = balance_actualy,
            description = description
        )


    return transaction_execute



def service_transfer(account_s, account_r, amount, transaction_transfer, description):
    with transaction.atomic():
        account_send = Account.objects.select_for_update().get(account_number=account_s)
        account_receive = Account.objects.select_for_update().get(account_number=account_r)
        
        balance_actualy_send = account_send.balance
        balance_actualy_recive = account_receive.balance
        account_send.balance -= amount
        account_send.save()
        account_receive.balance += amount
        account_receive.save()

        #transaccion para cuenta envio
        transfer = Transaction.objects.create(
            transaction_type = transaction_transfer,
            account = account_send,
            amount = amount,
            balance_after = balance_actualy_send,
            description = description,
            target_account = account_receive
        )

        #transaccion para cuenta recibe
        Transaction.objects.create(
            transaction_type = transaction_transfer,
            account = account_send,
            amount = amount,
            balance_after = balance_actualy_recive,
            description = description,
            target_account = account_receive
        )
    
    return transfer