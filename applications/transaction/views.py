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
from rest_framework import status
#
from rest_framework.authentication import TokenAuthentication
#
from rest_framework.permissions import IsAuthenticated
#
from .services import service_deposit, service_withdraw, service_transfer
# Create your views here.


class CreateTransactionApiView(CreateAPIView):
    serializer_class = TransactionSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializador = self.serializer_class(data=request.data)
        serializador.is_valid(raise_exception=True)
        #
        amount = serializador.validated_data['amount']
        description = serializador.validated_data['description']
        account = serializador.validated_data['account']

        try:        
            if serializador.validated_data['transaction_type'] == "DEPOSIT":                
                transaction_deposit = serializador.validated_data['transaction_type']   
                #
                deposit = service_deposit(account, amount, transaction_deposit, description)
                
                return Response(
                    {
                        'mensaje':'success',
                        'type_transfer_exist' : transaction_deposit,
                        'account' : account,
                        'amount_deposit' : amount,
                        'deposit_id' : deposit.id
                    },
                    status=status.HTTP_202_ACCEPTED
                )
            
            elif serializador.validated_data['transaction_type'] == "WITHDRAW":
                transaction_withdraw = serializador.validated_data['transaction_type']
                #
                withdraw = service_withdraw(account, amount, transaction_withdraw, description)

                return Response(
                    {
                        'mensaje':'success',
                        'type_transfer_exist' : transaction_withdraw,
                        'account' : account,
                        'amount_withdraw' : amount,
                        'withdraw_id' : withdraw.id
                    },
                    status=status.HTTP_202_ACCEPTED
                )
            
            elif serializador.validated_data['transaction_type'] == "TRANSFER":
                account_send = serializador.validated_data['account']
                account_receive = serializador.validated_data['target_account']
                transaction_transfer = serializador.validated_data['transaction_type']
                #
                transfer =  service_transfer(account_send, account_receive, amount, transaction_transfer, description)            
                
                return Response(
                    {
                        'mensaje':'success',
                        'type_transfer_exist' : serializador.validated_data['transaction_type'],
                        'account' : serializador.validated_data['account'],
                        'amount_transfer' : serializador.validated_data['amount'],
                        'transfer_id' : transfer.id
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