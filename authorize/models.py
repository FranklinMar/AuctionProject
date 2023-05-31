from django.db import models
from django.forms import Form, CharField

class Login(Form):
    login = CharField(label = 'login')
    password = CharField(label = 'пароль')

class Create_user(Form):
    login = CharField(label = 'login')
    password = CharField(label = 'пароль')
    email = CharField(label = 'email')
    image = CharField(label='фото')
    # image = FileField(allow_empty_file=False, widget=FileInput(attrs={
    #             'accept': '.jpg, .svg, .png, .gif',
    #             'id': 'file'
    #         }))
