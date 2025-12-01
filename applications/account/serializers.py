#
from rest_framework import serializers
#
from .models import Account, AccountType


class AccountSerializer(serializers.Serializer):
    owner = serializers.IntegerField()
    type = serializers.IntegerField()
    balance = serializers.IntegerField()

     



class AccountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountType
        fields = (
            'id',
            'name',
            'description',
        )