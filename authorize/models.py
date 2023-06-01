from django.db import models
from django.forms import Form, CharField, EmailField, PasswordInput, EmailInput, TextInput


class Login(Form):
    login = CharField(label='Email or Name', widget=TextInput(attrs={
        'class': 'bg-dark text-white form-control form-control-sm',
        'id': 'login',
        'placeholder': 'Email or Name'
    }), required=True)
    password = CharField(label='Password', widget=PasswordInput(attrs={
        'class': 'bg-dark text-white form-control form-control-sm',
        'id': 'password',
        'placeholder': 'Password'
    }), required=True)


class CreateUser(Form):
    username = CharField(label='Username', widget=TextInput(attrs={
        'class': 'bg-dark text-white form-control form-control-sm',
        'id': 'name',
        'placeholder': 'Name'
    }), required=True)
    email = EmailField(label='Email', widget=EmailInput(attrs={
        'class': 'bg-dark text-white form-control form-control-sm',
        'id': 'email',
        'placeholder': 'Email address'
    }), required=True, label_suffix="Email address")
    password = CharField(label='Password', widget=PasswordInput(attrs={
        'class': 'bg-dark text-white form-control form-control-sm',
        'id': 'password',
        'placeholder': 'Password'
    }), required=True)
    confirm_password = CharField(label='Confirm Password', widget=PasswordInput(attrs={
        'class': 'bg-dark text-white form-control form-control-sm',
        'id': 'confirm_password',
        'placeholder': 'Confirm Password'
    }), required=True)

    # image = FileField(allow_empty_file=False, widget=FileInput(attrs={
    #             'accept': '.jpg, .svg, .png, .gif',
    #             'id': 'file'
    #         }))