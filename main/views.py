from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def main(request):
    return HttpResponse('hello beach')

def about_us(request):
    return HttpResponse('I dont want say anything about us')