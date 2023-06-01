from django.http import HttpResponse
from main.models import Chat, User, Message
from bson.objectid import ObjectId
from django.shortcuts import render


def chat_id(request, id :str):
    user2 = User.find_one({"name": id})
    if not (user2 is None) and 'name' in request.session:
        user1 = User.find_one({"name": request.session['name']})
        chat = Chat.find_one_by_users(user1,user2)
        if request.method == 'POST':
            chat.send(Message.create(user1,request.POST.get('text', '')))
        if chat is None:
            chat = Chat.create(user1,user2)
        return render(request,'main/chat.html',{'chat':chat,'user2': chat.user1 \
            if chat.user2.name == request.session['name'] else chat.user2})
    return HttpResponse("<h1>Error<h1>")
