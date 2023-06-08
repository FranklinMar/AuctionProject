
from django.forms import Form, CharField, Textarea, TextInput, ImageField, FileInput, DecimalField, NumberInput, \
    DateTimeField, ValidationError, DateTimeInput
from datetime import datetime


class ItemForm(Form):
    name = CharField(label='Name', required=True, widget=TextInput(attrs={
        'class': 'mb-2 bg-dark text-white form-control form-control-sm',
        'placeholder': 'Name'
    }))
    description = CharField(label='Description', required=True, widget=Textarea(attrs={
        'class': 'mb-2 bg-dark text-white form-control form-control-sm',
        'placeholder': 'Description',
        'rows': '5'}))
    image = ImageField(label='Image', required=False, widget=FileInput(attrs={
        'class': 'form-control bg-dark text-white form-control-sm'
    }))


def date_validation(value):
    if value < datetime.utcnow():
        raise ValidationError("Deadline '%(value)' cannot be lower than current UTC '%(now)'", code='invalid',
                              params={'value': value, 'now': datetime.utcnow()})


class CreateAuction(Form):
    start_bid = DecimalField(label='Start Bid', min_value='1', max_digits='2', widget=NumberInput(attrs={
        'class': 'mb-2 bg-transparent text-white form-control form-control-sm',
        'placeholder': 'Start bid'
    }))
    start_date = DateTimeField(label='Launch date', validators=[date_validation], widget=DateTimeInput(attrs={
        'class': 'mb-2 bg-transparent text-white form-control form-control-sm',
        'placeholder': 'Launch date',
        'id': 'launch',
        # 'value': datetime.utcnow()
    }))
    deadline = DateTimeField(label='Deadline', validators=[date_validation], widget=DateTimeInput(attrs={
        'class': 'mb-2 bg-transparent text-white form-control form-control-sm',
        'placeholder': 'Deadline',
        'id': 'deadline',
        # 'value': datetime.utcnow()
    }))
