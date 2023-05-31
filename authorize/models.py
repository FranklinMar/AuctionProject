from django.db import models
from django.forms import Form, CharField, PasswordInput

class Login(Form):
    login = CharField(label = 'login')
    password = CharField(label = 'пароль',widget=PasswordInput)

class Create_user(Form):
    login = CharField(label = 'login')
    password = CharField(label = 'пароль',widget=PasswordInput)
    email = CharField(label = 'email')
    image = CharField(label='фото', required=False)
    # image = FileField(allow_empty_file=False, widget=FileInput(attrs={
    #             'accept': '.jpg, .svg, .png, .gif',
    #             'id': 'file'
    #         }))
