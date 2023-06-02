from django.db import models
from django.forms import Form, CharField, Textarea, TextInput, ImageField, FileInput


class ItemForm(Form):
    name = CharField(label='Name', required=True, widget=TextInput(attrs={
        'class': 'mb-2 bg-dark text-white form-control form-control-sm',
        'placeholder': 'Name'
    }))
    description = CharField(label='Description', required=True, widget=Textarea(attrs={
        'class': 'mb-2 bg-dark text-white form-control form-control-sm',
        'placeholder': 'Description',
        'rows': '5'}))
    image = ImageField(label='Image', required=True, widget=FileInput(attrs={
        'class': 'form-control bg-dark text-white form-control-sm'
    }))
