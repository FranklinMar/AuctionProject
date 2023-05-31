from django.urls import path
from authorize.views import login, exit

urlpatterns = [
    path('', login),
    path('/', exit),
]