from django.shortcuts import render
#
from django.db import transaction, IntegrityError 
#
from .serializers import AccountSerializer, AccountTypeSerializer
#
from .models import AccountType, Account
#
from applications.users.models import User
#
from rest_framework.generics import CreateAPIView, ListAPIView
#
from rest_framework.response import Response
#
from rest_framework import status
#
from .functions import number
# Create your views here.


class CreateAccountApiView(CreateAPIView):
    serializer_class = AccountSerializer

    def create(self, request, *args, **kwargs):
        serializador = self.serializer_class(data=request.data)
        serializador.is_valid(raise_exception=True)

        
        
        try:
            with transaction.atomic():
                number_account = number()   
                balance = serializador.validated_data['balance']
                usuario = User.objects.filter(id=serializador.validated_data['owner']).exists()
                tipo = AccountType.objects.filter(id=serializador.validated_data['type']).exists()

                if not usuario:
                    return Response(
                        {
                            'error' : 'El usuario no existe'
                        },
                        status= status.HTTP_400_BAD_REQUEST
                    )
                
                
                if not tipo:
                    return Response(
                        {
                            'error' : 'El tipo de cuenta no existe'
                        },
                        status= status.HTTP_400_BAD_REQUEST
                    )

                account = Account.objects.create(
                    account_number = number_account,
                    owner = User.objects.get(id=serializador.validated_data['owner']),
                    type = AccountType.objects.get(id=serializador.validated_data['type']),
                    balance = balance
                )

                account_data = {
                    'number':account.account_number,
                    'owner' : account.owner.username,
                    'type':account.type.name,
                    'name': account.type.get_name_display(),
                    'balance':account.balance
                }

                return Response(
                    {
                        'status' : 'success',
                        'user' : account_data
                    },
                    status= status.HTTP_201_CREATED
                )
            
        except IntegrityError as e:
            return Response(
                {
                    'status': 'error',
                    'message': 'Error: el número de cuenta ya existe'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        except Exception as e:
            return Response(
                {
                    'status': 'error',
                    'message': 'Error al crear la cuenta'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
