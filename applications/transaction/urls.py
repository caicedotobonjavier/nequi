#
from django.urls import path, re_path, include

app_name = 'transaction_app'

from . import views

urlpatterns = [
    path('new-transaction', views.CreateTransactionApiView.as_view(), name='new_transaction'),
    path('list-transaction', views.ListTransactionsApiView.as_view(), name='list_transaction'),
    path('list-user-transaction', views.ListTransactionsUserApiView.as_view(), name='list_user_transaction'),
]