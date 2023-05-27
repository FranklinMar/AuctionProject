from django.shortcuts import render
from django.http import HttpResponse
from .models import *


# Create your views here.
def home(request):
    # print(User.objects.first().items)
    users = DB["User"]
    # user = User("Den", "denisbereznuuk@gmail.com", 0)
    user = users.find_one()
    print(type(user["_id"]))
    return HttpResponse(f"<h1>Hello world<h1>{user['name']}")
