from django.shortcuts import render
#
from .serializers import TransactionSerializer, TransactionsListSerializer
#
from rest_framework.generics import CreateAPIView, ListAPIView
#
from django.db import transaction, IntegrityError
#
from .models import Transaction
#
from applications.account.models import Account
#
from rest_framework.response import Response
#
from django.db import transaction
#
from rest_framework import status
#
from rest_framework.authentication import TokenAuthentication
#
from rest_framework.permissions import IsAuthenticated
# Create your views here.


class CreateTransactionApiView(CreateAPIView):
    serializer_class = TransactionSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializador = self.serializer_class(data=request.data)
        serializador.is_valid(raise_exception=True)

        try:
            with transaction.atomic():      
                
                if serializador.validated_data['transaction_type'] == "DEPOSIT":
                    account_transaction = Account.objects.select_for_update().get(account_number=serializador.validated_data['account'])
                    balance_actualy = account_transaction.balance
                    account_transaction.balance += serializador.validated_data['amount']
                    account_transaction.save()


                    Transaction.objects.create(
                        transaction_type = serializador.validated_data['transaction_type'],
                        account = account_transaction,
                        amount = serializador.validated_data['amount'],
                        balance_after = balance_actualy,
                        description = serializador.validated_data['description']
                    )          

                    return Response(
                        {
                            'mensaje':'success',
                            'type_transfer_exist' : serializador.validated_data['transaction_type'],
                            'balance_after' : balance_actualy,
                            'account' : serializador.validated_data['account'],
                            'amount_deposit' : serializador.validated_data['amount'],
                            'amount_total' : account_transaction.balance
                        }
                    )
                elif serializador.validated_data['transaction_type'] == "WITHDRAW":
                    account_transaction = Account.objects.select_for_update().get(account_number=serializador.validated_data['account'])
                    balance_actualy = account_transaction.balance
                    account_transaction.balance -= serializador.validated_data['amount']
                    account_transaction.save()

                    Transaction.objects.create(
                        transaction_type = serializador.validated_data['transaction_type'],
                        account = account_transaction,
                        amount = serializador.validated_data['amount'],
                        balance_after = balance_actualy,
                        description = serializador.validated_data['description']
                    )

                    return Response(
                        {
                            'mensaje':'success',
                            'type_transfer_exist' : serializador.validated_data['transaction_type'],
                            'balance_after' : balance_actualy,
                            'account' : serializador.validated_data['account'],
                            'amount_withdraw' : serializador.validated_data['amount'],
                            'amount_total' : account_transaction.balance
                        }
                    )
                
                elif serializador.validated_data['transaction_type'] == "TRANSFER":
                                      
                    account_send = Account.objects.select_for_update().get(account_number=serializador.validated_data['account'])
                    account_receive = Account.objects.select_for_update().get(account_number=serializador.validated_data['target_account'])
                    
                    balance_actualy_send = account_send.balance
                    balance_actualy_recive = account_receive.balance

                    account_send.balance -= serializador.validated_data['amount']
                    account_send.save()

                    account_receive.balance += serializador.validated_data['amount']
                    account_receive.save()

                    #transaccion para cuenta envio
                    Transaction.objects.create(
                        transaction_type = serializador.validated_data['transaction_type'],
                        account = account_send,
                        amount = serializador.validated_data['amount'],
                        balance_after = balance_actualy_send,
                        description = serializador.validated_data['description'],
                        target_account = account_receive
                    )

                    #transaccion para cuenta recibe
                    Transaction.objects.create(
                        transaction_type = serializador.validated_data['transaction_type'],
                        account = account_send,
                        amount = serializador.validated_data['amount'],
                        balance_after = balance_actualy_recive,
                        description = serializador.validated_data['description'],
                        target_account = account_receive
                    )


                    return Response(
                        {
                            'mensaje':'success',
                            'type_transfer_exist' : serializador.validated_data['transaction_type'],
                            'account' : serializador.validated_data['account'],
                            'balance_actualy' : balance_actualy_send,
                            'amount_transfer' : serializador.validated_data['amount'],
                            'balance' : account_send.balance
                        },
                        status=status.HTTP_202_ACCEPTED
                    )
            

        except IntegrityError as e:
            return Response(
                {
                    'status': 'error',
                    'message': 'Error: no se logro realizar la transaccion'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
            
        except Exception as e:
            print('Este es el error', e)
            return Response(
                {
                    'error' : 'error'
                }
            )


class ListTransactionsApiView(ListAPIView):
    serializer_class = TransactionsListSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        print(user)
        return Transaction.objects.all()
    


class ListTransactionsUserApiView(ListAPIView):
    serializer_class = TransactionsListSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(account__owner=user)