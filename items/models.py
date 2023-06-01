from django.db import models
from django.forms import Form, CharField, Textarea

class Item_form(Form):
    name = CharField(label='Name', required=True)
    description = CharField(label='Description', required=True,widget=Textarea(attrs={"rows":"5"}))
    image = CharField(label='Image', required=True)