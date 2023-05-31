from django.shortcuts import render
from main.models import User
from django.contrib.auth.hashers import make_password
from authorize.models import *
from django.views.decorators.cache import never_cache
from django.http import HttpResponseRedirect


@never_cache
def login(request):
    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            user = User.find_one({'name': form.cleaned_data['login']})
            if not (user is None) and user.password == make_password(form.cleaned_data['password']):
                request.session['name'] = user.name
                request.session['image'] = user.image
                return HttpResponseRedirect(request.POST.get('back', ''))
            return render(request, 'main/signin.html', {'back': request.POST.get('back', ''), 'form': Login(),
                                                      'error': 'Неправильний пароль або логін'})
    return render(request, 'main/signin.html', {'back': request.POST.get('back', ''), 'form': Login()})


def logout(request):
    request.session.pop('name')
    request.session.pop('image')
    return HttpResponseRedirect('/')


@never_cache
def create_user(request):
    if request.method == 'POST':
        form = CreateUser(request.POST)
        if form.is_valid():
            try:
                user = User.create(form.cleaned_data['login'], form.cleaned_data['password'],
                                   form.cleaned_data['email'])  # , image=form.cleaned_data['image'])
                request.session['name'] = user.name
                return HttpResponseRedirect(request.POST.get('back', ''))
            except ValueError as error:
                return render(request, 'main/signup.html', {'back': request.POST.get('back', ''),
                                            'form': CreateUser(), 'error': error})
    return render(request, 'main/signup.html', {'back': request.POST.get('back', ''), 'form': CreateUser()})