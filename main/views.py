from django.shortcuts import render
from django.http import HttpResponse
from .models import *


# Create your views here.
def home(request):
    # print(User.objects.first().items)
    users = DB["User"]
    user = users.find_one()
    return HttpResponse(f"<h1>Hello world<h1>{user['name']}")
