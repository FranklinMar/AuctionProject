from django.shortcuts import render
from django.http import HttpResponse
from main.models import User

# Create your views here.

def user_id(request, id :str):
    user = User.find_one({"name": id})
    if user is None:
        return HttpResponse("<h1>Error<h1>")
    return HttpResponse("<p>name:"+user.name+"</p>")

def settings(request, id :str):
    if 'name' in request.session and request.session['name'] == id:
        user = User.find_one({"name": id})
        if not (user is None):
            return HttpResponse("<p>name:" + user.name + ", settings</p>")
    return HttpResponse("<h1>Error<h1>")