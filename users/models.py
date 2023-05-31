from django.db import models
from django.forms import Form, FileField, FileInput, CharField, PasswordInput

class Change_email(Form):
    email = CharField(label = 'email')

class Change_password(Form):
    password = CharField(label='пароль',widget=PasswordInput)

class Change_image(Form):
    image = CharField(label='фото')
    # image = FileField(allow_empty_file=False, widget=FileInput(attrs={
    #             'accept': '.jpg, .svg, .png, .gif',
    #             'id': 'file'
    #         }))
