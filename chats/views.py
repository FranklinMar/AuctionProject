from django.shortcuts import render
from django.http import HttpResponse
from main.models import Chat
from bson.objectid import ObjectId

def chat_id(request, id :str):
    chat = Chat.find_one({"_id": ObjectId(id)})
    if not (chat is None):
        # if ('name' in request.session and chat.user1.name == request.session['name']) or \
        # ('name' in request.session and chat.user1.name == request.session['name']):
            return HttpResponse("<h1>chat id:"+str(chat.id)+"</p><p>"+chat.user1.name+"</p><p>"+chat.user2.name+"</p>")
    return HttpResponse("<h1>Error<h1>")