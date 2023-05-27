from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def item_id(request, id :str):
    return HttpResponse("<h1>item: "+id+"<h1>")

def auction(request, id :str):
    return HttpResponse("<h1>auction of item: "+id+"<h1>")