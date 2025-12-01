from django.db import models
#
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
#
from .managers import UserManager
# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('User Name', max_length=100)
    email = models.EmailField('Email', max_length=254, unique=True)
    document = models.CharField('Documet', max_length=20, unique=True)
    phone = models.CharField('Phone', max_length=20, blank=True, null=True)
    address = models.CharField('Address', max_length=50, blank=True, null=True)

    is_active = models.BooleanField('Active', default=False)
    is_staff = models.BooleanField('Staff', default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'document']
    
    
    def __str__(self):
        return f'{self.username}'
