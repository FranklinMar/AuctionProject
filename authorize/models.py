from django.db import models
from django.forms import Form, CharField

class Login(Form):
    login = CharField(label = 'login')
    password = CharField(label = 'пароль')
