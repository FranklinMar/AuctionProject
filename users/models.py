from django.db import models
from django.forms import Form, CharField, PasswordInput, EmailInput, ImageField, FileInput


class Change_email(Form):
    email = CharField(label='Email Address', widget=EmailInput(attrs={
        'class': 'form-control bg-dark text-white form-control-sm'
    }))


class Change_password(Form):
    password = CharField(label='Password', widget=PasswordInput(attrs={
        'class': 'form-control bg-dark text-white form-control-sm'
    }))


class Change_image(Form):
    image = ImageField(widget=FileInput(attrs={
        'class': 'form-control bg-dark text-white form-control-sm mt-2 mb-2',
        'style': 'width:100%; max-width: 1000px'
    }))
    # image = FileField(allow_empty_file=False, widget=FileInput(attrs={
    #             'accept': '.jpg, .svg, .png, .gif',
    #             'id': 'file'
    #         }))
