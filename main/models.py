import datetime

from django.db import models

from django.conf import settings
# Create your models here.
# from djongo import models
# from django.core.exceptions import ValidationError
# from django.utils import timezone
# from djangotoolbox.fields import ListField


# def min_value_allowed(value):
#     if value >= 0:
#         return True
#     else:
#         raise ValidationError('Only positive numbers')
#
#
# class Item(models.Model):
#     _id = models.ObjectIdField()
#     name = models.CharField('Назва', max_length=30, unique=True)
#
#     def __getitem__(self, name):
#         return getattr(self, name)
#
#     class Meta:
#         abstract = True
#         managed = False
#         db_table = 'Item'
#
#
# class Chat(models.Model):
#     _id = models.ObjectIdField()
#     name = models.CharField('Назва', max_length=30)
#
#     def __getitem__(self, name):
#         return getattr(self, name)
#
#     class Meta:
#         abstract = True
#         managed = False
#         db_table = 'Chat'
#
#
# class User(models.Model):
#     _id = models.ObjectIdField()
#     name = models.CharField('Ім\'я', max_length=30, unique=True)
#     email = models.EmailField('Email', max_length=30, unique=True)
#     role = models.CharField('Role', max_length=5, default='user')
#     image = models.ImageField('Фото', upload_to='media/')
#     balance = models.FloatField('Гроші', default=0, validators=[min_value_allowed])
#     items = models.ArrayField(Item)
#     chats = models.ArrayField(Chat)
#     date_modified = models.DateTimeField(auto_now_add=True, blank=True)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         db_table = 'User'
#
#     objects = models.DjongoManager()
