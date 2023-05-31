from django.urls import path
from authorize.views import login, logout, create_user

urlpatterns = [
    path('login/', login, name='Login'),
    path('logout/', logout, name='Logout'),
    path('register/', create_user, name='Register'),
]