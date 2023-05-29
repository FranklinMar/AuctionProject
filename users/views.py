from django.shortcuts import render
from django.http import HttpResponse
from main.models import User
from pymongo import MongoClient
from AuctionProject.secret import CONNECTION_STRING
from AuctionProject.secret import CONNECTION_STRING

# Create your views here.

def user_id(request, id :str):
    d = MongoClient(CONNECTION_STRING)['Auction']['User'].find_one({"name":id},  no_cursor_timeout=True)
    print(d)
    user = User.find_one({"name": id})
    print(3)
    if user is None:
        return HttpResponse("<h1>Error<h1>")
    return HttpResponse("<h1>id:"+user.id+"<h1><p>name:"+user.name+"</p>")

def settings(request, id :str):
    if 'name' in request.session and request.session['name'] == id:
        user = User.find_one({"name": id})
        if not (user is None):
            return HttpResponse("<h1>id:" + user.id + "<h1><p>name:" + user.name + ", settings</p>")
    return HttpResponse("<h1>Error<h1>")