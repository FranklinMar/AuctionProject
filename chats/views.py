import json

from django.http import HttpResponse
from main.models import Chat, User, Message
from bson.objectid import ObjectId
from django.shortcuts import render
from django.views.decorators.cache import never_cache
from asgiref.sync import sync_to_async


@never_cache
def chats(request):
    if 'user' not in request.session:
        return render(request, 'main/error.html')
    this_user = User.find_one({"name": request.session['user']['name']})
    contact_list = [User.find_one({'_id': item.user2.id if this_user.id == item.user1.id else item.user1.id})
                    for item in this_user.chats_list()]
    return render(request, 'chats/chat.html', {'user': this_user, 'contacts': contact_list})


@never_cache
def chat_id(request, id: str):
    other_user = User.find_one({"name": id})
    if not other_user or 'user' not in request.session:
        return render(request, 'main/error.html')

    this_user = User.find_one({"name": request.session['user']['name']})
    chat = Chat.find_one_by_users(this_user, other_user)
    if request.method == 'POST':
        chat.send(Message.create(request.POST.get('text', ''), ObjectId(this_user.id)))
    if chat is None:
        chat = Chat.create(this_user, other_user)
        this_user.chats.append(chat.id)
        this_user.save()
        other_user.chats.append(chat.id)
        other_user.save()

    contact_list = [User.find_one({'_id': item.user2.id if this_user.id == item.user1.id else item.user1.id})
                    for item in this_user.chats_list()]  # [Chat.find({'_id': {'$in': }})]
    return render(request, 'chats/chat.html', {'user': this_user, 'chat': chat,
                                               'other_user': other_user, 'contacts': contact_list})
    # return HttpResponse("<h1>Error<h1>")


@sync_to_async
@never_cache
def online(request, id):
    user = User.find_one({'_id': id})
    json_data = json.dumps(user.online if user else None)
    return HttpResponse(json_data, content_type="application/json")
