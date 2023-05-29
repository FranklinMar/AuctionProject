from django.shortcuts import render
from django.http import HttpResponse
from main.models import Chat
# Create your views here.

def chat_id(request, id :str):
        chat = Chat.find_one({"_id": id})
        if not (chat is None):
            for user in chat.users_list():
                if 'name' in request.session and user.name == request.session['name']:
                    return HttpResponse("<h1>chat id:"+chat.id+"</p>")
        return HttpResponse("<h1>Error<h1>")