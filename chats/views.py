from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def chat_id(request, id :str):
    return HttpResponse("<h1>chat: "+id+"<h1>")