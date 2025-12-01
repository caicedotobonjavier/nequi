#Serializers
from rest_framework import serializers
#
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField()
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'document',
            'phone',
            'address',            
        )



class LoginUserSerializer(serializers.Serializer):
    user = serializers.EmailField()
    password = serializers.CharField()
