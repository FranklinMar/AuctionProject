from django.shortcuts import render
from django.http import HttpResponse
# from .models import User


# Create your views here.
def home(request):
    # print(User.objects.first().items)
    return HttpResponse(f"<h1>Hello world<h1>")
