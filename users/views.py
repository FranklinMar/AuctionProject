from django.shortcuts import render
from django.http import HttpResponse
from main.models import User
from users.models import *
from django.views.decorators.csrf import csrf_protect


def user_id(request, id: str):
    user = User.find_one({"name": id})
    if user is None:
        return HttpResponse("<h1>Error<h1>")
    return render(request, 'main/user.html', {'user':user
        ,'is_own': 'name' in request.session and request.session['name'] == user.name})


def settings(request, id: str):
    user = User.find_one({"name": id})
    if not (user is None) and 'name' in request.session and request.session['name'] == user.name:
        if request.method == 'POST':
            form = Change_email(request.POST)
            if form.is_valid():
                user.email = form.cleaned_data['email']
            form = Change_password(request.POST)
            if form.is_valid():
                user.password = form.cleaned_data['password']
            form = Change_image(request.POST, request.FILES)
            if form.is_valid():
                user.image = form.cleaned_data['image']
                request.session['image'] = user.image
        return render(request, 'main/user_settings.html', {'user':user,\
                                                           'email_form':Change_email(initial={'email':user.email}),\
                                                           'password_form':Change_password(),\
                                                           'image_form':Change_image()})
    return HttpResponse("<h1>Error<h1>")