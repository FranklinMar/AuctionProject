from django.shortcuts import render
from django.http import HttpResponse
from main.models import User
from users.forms import *
from django.views.decorators.csrf import csrf_protect


def user_profile(request, id: str):
    user = User.find_one({"name": id})
    if user is None:
        return HttpResponse("<h1>Error<h1>")
    return render(request, 'user/user.html', {'user': user
        ,'is_own': 'name' in request.session and request.session['name'] == user.name})


def user_settings(request, id: str):
    user = User.find_one({"name": id})
    if not (user is None) and 'name' in request.session and request.session['name'] == user.name:
        if request.method == 'POST':
            form = ChangeEmail(request.POST)
            if form.is_valid():
                user.email = form.cleaned_data['email']
            form = ChangePassword(request.POST)
            if form.is_valid():
                user.password = form.cleaned_data['password']
            form = ChangeImage(request.POST, request.FILES)
            if form.is_valid():
                user.image = form.cleaned_data['image']
                request.session['image'] = user.image
        return render(request, 'user/user_settings.html', {'user': user,
                                                           'email_form': ChangeEmail(initial={'email': user.email}),
                                                           'password_form': ChangePassword(),
                                                           'image_form': ChangeImage()})
    return HttpResponse("<h1>Error<h1>")
