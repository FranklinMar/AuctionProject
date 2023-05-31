from django.shortcuts import render
from main.models import User, hash
from authorize.models import *
from django.http import HttpResponseRedirect

def login(request):
    form = Login(request.POST)
    if form.is_valid():
        user = User.find_one({'name':form.cleaned_data['login']})
        if not (user is None) and user.password == hash(form.cleaned_data['password']):
            request.session['name'] = user.name
            return HttpResponseRedirect(request.POST.get('back',''))
        return render(request, 'main/login.html',{'back': request.POST.get('back',''), 'Login':Login(),\
                                                  'error': 'неправильний пароль або логін'})
    return render(request, 'main/login.html', {'back': request.POST.get('back',''), 'Login':Login()})

def exit(request):
    request.session.pop('name')
    return HttpResponseRedirect(request.POST.get('back', ''))

def create_user(request):
    form = Create_user(request.POST)
    if form.is_valid():
        try:
            user = User.create(form.cleaned_data['login'],form.cleaned_data['password'],form.cleaned_data['email'],
                               image=form.cleaned_data['image'])
            request.session['name'] = user.name
            return HttpResponseRedirect(request.POST.get('back', ''))
        except ValueError as error:
            return render(request, 'main/create_user.html', {'back': request.POST.get('back', ''),
                                                             'create': Create_user(),
                                                             'error': error})
    return render(request, 'main/create_user.html', {'back': request.POST.get('back', ''), 'Login': Create_user()})
