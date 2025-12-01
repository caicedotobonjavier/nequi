from django.urls import path, re_path, include

app_name = 'account_app'

from . import views

urlpatterns = [
    path('create-account', views.CreateAccountApiView.as_view(), name='create_account'),
]