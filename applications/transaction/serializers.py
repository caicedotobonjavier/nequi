#
from .models import Transaction
#
from applications.account.models import Account
#
from rest_framework import serializers


class TransactionSerializer(serializers.Serializer):
    transaction_type = serializers.CharField()
    account = serializers.CharField()
    amount = serializers.IntegerField()    
    description = serializers.CharField()
    target_account = serializers.IntegerField()

    def validate_transaction_type(self, value):
        if value not in ["DEPOSIT", "WITHDRAW", "TRANSFER"]:
            raise serializers.ValidationError('Not exist this type of transaction')
        return value
    
    def validate_account(self, value):
        acc = Account.objects.filter(account_number=value).exists()
        if not acc:
            raise serializers.ValidationError('Not exist account')
        return value
    

    def validate_target_account(self, value):
        if value == "TRANSFER":
            if not Account.objects.filter(account_number=value).exists():
                raise serializers.ValidationError('Not exist account')
        return value


    def validate(self, data):
        transaction_type = data['transaction_type']
        account_number = data['account']
        amount = data["amount"]

        account_origen = Account.objects.get(account_number=data['account'])

        if transaction_type == "WITHDRAW":
            if amount > account_origen.balance:
                raise serializers.ValidationError('El monto es mayor al saldo actual')
        
        elif transaction_type == "TRANSFER":
            target_account = data['target_account']

            if not target_account:
                raise serializers.ValidationError('Es requerida una cuenta de envio para realizar la transferencia')
            
            if str(account_number) == str(target_account):
                raise serializers.ValidationError('No se puede hacer una transferencia a la misma cuenta')
            
            if amount > account_origen.balance:
                raise serializers.ValidationError('El monto es mayor al saldo actual')
            
            if amount <= 0:
                raise serializers.ValidationError('No se puede realizar transferencia de $0 o menor')
            
            if not Account.objects.filter(account_number=target_account).exists():
                raise serializers.ValidationError('La cuenta de destino no existe')
        
        elif transaction_type == "DEPOSIT":
            if amount <= 0:
                raise serializers.ValidationError('No se pueden realizar depositos de $0')

        return data
     


class TransactionsListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    class Meta:
        model = Transaction
        fields = (
            'id',
            'transaction_type',
            'account',
            'user',            
            'amount',
            'balance_after',
            'timestamp',
            'description',
            'target_account',                        
        )

    def get_user(self, obj):
        return f'{obj.account.owner}'