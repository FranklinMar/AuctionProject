from django.shortcuts import render, redirect
from main.models import User
from authorize.forms import *
from django.views.decorators.cache import never_cache


@never_cache
def login(request):
    if 'user' in request.session:
        return redirect('Home')
    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            user = User.find_one({'name': form.cleaned_data['login']})
            if user is None:
                return render(request, 'auth/signin.html', {'back': request.POST.get('back', ''), 'form': Login(),
                                                            'error': 'Invalid username or password'})
            if not(user.try_login(form.cleaned_data['password'])):
                return render(request, 'auth/signin.html', {'back': request.POST.get('back', ''), 'form': Login(),
                                                            'error': 'Invalid password'})
            request.session['user'] = user.get_vars_with_id()
            return redirect('Home')
    return render(request, 'auth/signin.html', {'back': request.POST.get('back', ''), 'form': Login()})


def logout(request):
    if 'user' in request.session:
        request.session.pop('user')
    return redirect('Home')


@never_cache
def create_user(request):
    if 'user' in request.session:
        return redirect('Home')
    if request.method == 'POST':
        form = CreateUser(request.POST)
        if form.is_valid():
            try:
                user = User.create(form.cleaned_data['username'], form.cleaned_data['password'],
                                   form.cleaned_data['email'])  # , image=form.cleaned_data['image'])
                request.session['user'] = user.get_vars_with_id()
                return redirect('Home')
            except ValueError as error:
                return render(request, 'auth/signup.html', {'back': request.POST.get('back', ''),
                                            'form': CreateUser(), 'error': error})
    return render(request, 'auth/signup.html', {'back': request.POST.get('back', ''), 'form': CreateUser()})
