from django.db import models
from django.forms import Form, CharField, Textarea, TextInput, ImageField, FileInput


class Item_form(Form):
    name = CharField(label='Name', widget=TextInput(attrs={
        'class': 'mb-2 bg-dark text-white form-control form-control-sm',
        'placeholder': 'Name'
    }), required=True)
    description = CharField(label='Description', required=True, widget=Textarea(attrs={
        'class': 'mb-2 bg-dark text-white form-control form-control-sm',
        'placeholder': 'Description',
        'rows': '5',
        'value': ''}))
    image = ImageField(label='Image', widget=FileInput(attrs={
        'class': 'form-control bg-dark text-white form-control-sm'
    }))