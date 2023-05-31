from django.urls import path
from authorize.views import login, logout, create_user

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', create_user, name='register'),
]
