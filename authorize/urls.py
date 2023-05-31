from django.urls import path
from authorize.views import login, exit, create_user

urlpatterns = [
    path('login/', login),
    path('exit/', exit),
    path('create/', create_user),
]