from django.db import models
from  django import forms

class Change_email(forms.Form):
    email = forms.CharField(label = 'email')

class Change_password(forms.Form):
    password = forms.CharField(label='пароль',widget=forms.PasswordInput)

class Change_image(forms.Form):
    image = forms.CharField(label='фото')
    # image = forms.FileField(allow_empty_file=False, widget=FileInput(attrs={
    #             'accept': '.jpg, .svg, .png, .gif',
    #             'id': 'file'
    #         }))
