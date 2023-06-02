from django.shortcuts import render, redirect
from main.models import User
from django.contrib.auth.hashers import make_password, check_password
from authorize.forms import *
from django.views.decorators.cache import never_cache
from django.http import HttpResponseRedirect


@never_cache
def login(request):
    if 'name' in request.session:
        return redirect('Home')
    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            user = User.find_one({'name': form.cleaned_data['login']})
            if user is None:
                return render(request, 'auth/signin.html', {'back': request.POST.get('back', ''), 'form': Login(),
                                                            'error': 'Неправильний логін'})
            if not(check_password(form.cleaned_data['password'], user.password)):
                return render(request, 'auth/signin.html', {'back': request.POST.get('back', ''), 'form': Login(),
                                                            'error': 'Неправильний пароль'})
            request.session['name'] = user.name
            request.session['image'] = user.image
            print(2)
            print(request.POST.get('back', ''))
            return redirect(request.POST.get('back', ''))
    return render(request, 'auth/signin.html', {'back': request.POST.get('back', ''), 'form': Login()})


def logout(request):
    request.session.pop('name')
    request.session.pop('image')
    return redirect('Home')


@never_cache
def create_user(request):
    if 'name' in request.session:
        return redirect('Home')
    # print(1)
    print(request.POST.get('back', ''))
    if request.method == 'POST':
        form = CreateUser(request.POST)
        if form.is_valid():
            try:
                user = User.create(form.cleaned_data['username'], form.cleaned_data['password'],
                                   form.cleaned_data['email'])  # , image=form.cleaned_data['image'])
                request.session['name'] = user.name
                request.session['image'] = user.image
                return HttpResponseRedirect(request.POST.get('back', ''))
            except ValueError as error:
                return render(request, 'auth/signup.html', {'back': request.POST.get('back', ''),
                                            'form': CreateUser(), 'error': error})
    return render(request, 'auth/signup.html', {'back': request.POST.get('back', ''), 'form': CreateUser()})
