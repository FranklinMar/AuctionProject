import datetime

from django.db import models

from django.conf import settings
# Create your models here.
from djongo import models
from django.core.exceptions import ValidationError
from django.utils import timezone
# from djangotoolbox.fields import ListField


def min_value_allowed(value):
    if value >= 0:
        return True
    else:
        raise ValidationError('Only positive numbers')


# class Item(models.Model):
#     name = models.CharField('Назва', unique=True)
#
#     class Meta:
#         abstract = True
#         db_table = 'Item'
#
#
# class Chat(models.Model):
#     name = models.CharField('Назва')
#
#     class Meta:
#         abstract = True
#         db_table = 'Chat'


class User(models.Model):
    name = models.CharField('Ім\'я', max_length=30, unique=True)
    email = models.EmailField('Email', max_length=30, unique=True)
    role = models.CharField('Role', max_length=5, default='user')
    image = models.ImageField('Фото', upload_to='media/')
    balance = models.FloatField('Гроші', default=0, validators=[min_value_allowed])
    # items = models.ArrayField(model_container=Item, blank=True)
    # chats = models.ArrayField(model_container=Chat, blank=True)
    date_modified = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'User'


Object = models.DjongoManager()
