from django.http import HttpResponse
from main.models import Chat
from bson.objectid import ObjectId
from django.shortcuts import render

def chat_id(request, id :str):
    chat = Chat.find_one({"_id": ObjectId(id)})
    if not (chat is None):
        if ('name' in request.session and chat.user1.name == request.session['name']) or \
        ('name' in request.session and chat.user1.name == request.session['name']):
            return render(request,'main/chat.html',{'chat':chat,'user2':
                chat.user1 if chat.user2.name == request.session['name'] else chat.user2})
    return HttpResponse("<h1>Error<h1>")