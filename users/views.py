from django.shortcuts import render
from django.http import HttpResponse
from main.models import User
from users.models import *

# Create your views here.

def user_id(request, id :str):
    user = User.find_one({"name": id})
    if user is None:
        return HttpResponse("<h1>Error<h1>")
    return render(request, 'main/user.html', {'user':user})

def settings(request, id :str):
        user = User.find_one({"name": id})
        if not (user is None):
            if request.method == 'POST':
                form = Change_email(request.POST)
                if form.is_valid():
                    user.update({'$set':{'email':form.cleaned_data['email']}})
                    user = User.find_one({'_id':user.id})
                form = Change_password(request.POST)
                if form.is_valid():
                    user.update({'$set': {'password': hash(form.cleaned_data['password'])}})
                    user = User.find_one({'_id': user.id})
                form = Change_image(request.POST)
                if form.is_valid():
                    user.update({'$set': {'image': form.cleaned_data['image']}})
                    user = User.find_one({'_id': user.id})
            return render(request, 'main/user_settings.html', {'user':user,\
                                                               'email_form':Change_email(initial={'email':user.email}),\
                                                               'password_form':Change_password(),\
                                                               'image_form':Change_image()})
        return HttpResponse("<h1>Error<h1>")