from django.db import models

from django.conf import settings
# Create your models here.
from mongoengine import *

connect(host=settings.DATABASES['default']['HOST'])


class User(Document):
    name = StringField(unique=True)
    email = EmailField(unique=True)
    role = StringField(default='user')
    image = StringField(default='')
    balance = Decimal128Field(default=0, min_value=0)
    items = ListField()
    chats = ListField()

    meta = {'db_alias': 'user'}
