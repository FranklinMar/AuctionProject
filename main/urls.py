from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='Home'),
    path('error', views.error, name='Error')
]
