from django.urls import path, re_path, include

app_name = 'users_app'

from . import views

urlpatterns = [
    path('create-user', views.CreateUserApiView.as_view(), name='create_user'),
    path('list-user', views.ListUserApiView.as_view(), name='list_user'),
    path('login-user', views.LoginApiView.as_view(), name='login_user'),
]
