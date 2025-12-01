from django.shortcuts import render
#
from .models import User
#
from django.contrib.auth import login, logout, authenticate
#
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView
#
from rest_framework.views import APIView
#
from .serializers import UserSerializer, LoginUserSerializer
#
from rest_framework.response import Response
#
from rest_framework.authtoken.models import Token
#
from rest_framework import status
# Create your views here.


class CreateUserApiView(CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializador = self.serializer_class(data=request.data)
        serializador.is_valid(raise_exception=True)
        
        #recupero los datos del serializador y los almaceno en una variable
        username = serializador.validated_data['username']
        email = serializador.validated_data['email']
        document = serializador.validated_data['document']
        password = serializador.validated_data['password']
        phone = serializador.validated_data['phone']
        address = serializador.validated_data['address']

        user = User.objects.create_user(
            username,
            email,
            document,
            password,
            phone = phone,
            address = address
        )

        token = Token.objects.create(
            user = user
        )

        data_user = {
            'user' : user.username,
            'email' : user.email,
            'access_token' : token.key
        }
        
        return Response(
            {
                'status' : status.HTTP_200_OK,
                'created_user' : 'OK',
                'user' : data_user
            }
        )




class ListUserApiView(ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()


class LoginApiView(APIView):
    serializer_class = LoginUserSerializer
    
    def post(self, request):
        serializador = self.serializer_class(data=request.data)
        serializador.is_valid(raise_exception=True)

        user = serializador.validated_data['user']
        password = serializador.validated_data['password']

        user = authenticate(
            username=user,
            password=password
        )

        if not user:
            return Response(
                {
                    'error':'Credeciales incorrectas'
                }, 
                status=status.HTTP_401_UNAUTHORIZED
            )


        token, created = Token.objects.get_or_create(user=user)

        print(token)
        print(token.key)
        print(created)


        return Response(
            {
                'msj' : "success",
                'user' : user.username,
                'user_email' : user.email,
                'token_id' : token.key,
                'ip': request.META.get("REMOTE_ADDR"),
                'indications' : 'el siguiente es el link para las transacciones, recurde usar su token_id',
                'link' : 'http://127.0.0.1:8000/api-transaction/new-transaction',
                'user_method' : 'POST',
                'transaction_options' : '"DEPOSIT", "WITHDRAW", "TRANSFER"'
            },
            status=status.HTTP_200_OK
        )