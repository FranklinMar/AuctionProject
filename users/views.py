from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def user_id(request, id :str):
    return HttpResponse("<h1>Your id is "+id+"<h1>")

def settings(request, id :str):
    return HttpResponse("<h1>settings of user: "+id+"<h1>")