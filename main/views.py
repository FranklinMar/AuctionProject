from django.shortcuts import render
from django.http import HttpResponse
from .models import User


# Create your views here.
def home(request):
    return HttpResponse(f"<h1>Hello world<h1>{User.objects.first().name}")
