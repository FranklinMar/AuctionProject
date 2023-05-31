import datetime
from functools import partial

from bson import ObjectId
from AuctionProject.settings import MEDIA_ROOT
from AuctionProject.settings import MEDIA_ROOT
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from pymongo import MongoClient
from django.core.validators import validate_email
from django.conf import settings
# Create your models here.
# from djongo import models
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password  # , check_password
from django.contrib.auth.password_validation import validate_password
from django.core.files.storage import FileSystemStorage
from PIL import Image
import hashlib
from datetime import datetime
# from django.utils import timezone
# from djangotoolbox.fields import ListField
CLIENT = MongoClient(settings.DATABASES['default']['CONNECTION'])
DB = CLIENT[settings.DATABASES['default']['NAME']]

Default_image_url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTFUw3mx3zKkMbGCQriCSpAH-ZUAoxur55odw&usqp=CAU'

def hash_file(file, block_size=65536):
    hasher = hashlib.sha256()
    for buf in iter(partial(file.read, block_size), b''):
        hasher.update(buf)
    return hasher.hexdigest()

def hash(text):
    hash = hashlib.sha256()
    hash.update(text.encode())
    return str(hash.hexdigest())

class User:
    __collection = DB['User']
    # __items = DB['Item']
    # __chats = DB['Chat']
    __roles = ('admin', 'mod', 'user', 'guest')

    def __init__(self, document):
        self.__name = document['name']
        self.__password = document['password']
        self.__email = document['email']
        self.__balance = float(document['balance']) if 'balance' in document else 0
        self.__role = document['role'] if 'role' in document else 'user'
        self.__image = document['image'] if 'image' in document else Default_image_url
        self.items = document['items'] if 'items' in document else []
        self.chats = document['chats'] if 'chats' in document else []
        self.__id = document['_id']

    def update(self, set):
        return self.__collection.update_one({"_id": self.__id}, set)

    def delete(self):
        return self.__collection.delete_one(filter={"_id": self.__id})

    def get_vars(self):
        return {key.replace('_User__', ''): self.__dict__[key] for key in self.__dict__}

    def try_login(self, password):
        return make_password(password) == self.password

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError(f"Property type must be 'str', not '{type(value).__name__}'")
        self.__name = value

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        if not isinstance(value, str):
            raise TypeError(f"Property type must be 'str', not '{type(value).__name__}'")
        self.__password = hash(value)
        self.update({'$set': {'password': self.__password}})

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        if not isinstance(value, str):
            raise TypeError(f"Property type must be 'str', not '{type(value).__name__}'")
        validate_email(value)
        self.__email = value
        self.update({'$set': {'email': self.__email}})

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError(f"Property type must be a 'int' or 'float', not '{type(value).__name__}'")
        if value < 0:
            raise ValidationError('Not negative error')
        self.__balance = value

    @property
    def role(self):
        return self.__role

    @role.setter
    def role(self, value):
        if not isinstance(value, str):
            raise TypeError(f"Property type must be 'str', not '{type(value).__name__}'")
        if value not in self.__roles:
            raise ValidationError('Role not found')
        self.__role = value

    @property
    def image(self):
        return self.__image

    @image.setter
    def image(self, value):
        file_storage = FileSystemStorage()
        if isinstance(value, str):
            # if not file_storage.exists(value):
            #     raise ValidationError('File does not exist in a storage')
            filename = value
        elif isinstance(value, InMemoryUploadedFile):
            image = Image.open(value)
            image.verify()
            filename = f'images/users/{hash_file(value)}.{value.content_type.split("/")[-1]}'
            if not file_storage.exists(filename):
                file_storage.save(filename, value)
            filename = str(MEDIA_ROOT) + "/" + filename
        else:
            raise TypeError(f"Property type must be 'str' or 'InMemoryUploadedFile', not '{type(value).__name__}'")
        self.__image = filename
        self.update({'$set': {'image': self.__image}})

    @property
    def items(self):
        return self.__items

    def items_list(self):
        return [Item(**document) for document in DB['Item'].find({"_id": {"$in": self.__items}})]

    @items.setter
    def items(self, value):
        if not isinstance(value, list):
            raise TypeError(f"Property type must be a list of 'str', not '{type(value).__name__}'")
        if not all(isinstance(item, ObjectId) for item in value):
            raise TypeError(f"Property type inside list must be 'ObjectId'")
        if len(value) != len(list(DB['Item'].find({"_id": {"$in": value}}))):
            # items_collection = DB['Item']
            # if len(value) != len([items_collection.find_one({"_id": item}) for item in value]):
            raise ValidationError("Not all items found")
        self.__items = value

    @property
    def chats(self):
        return self.__chats

    @chats.setter
    def chats(self, value):
        if not isinstance(value, list):
            raise TypeError(f"Property type must be a list of 'str', not '{type(value).__name__}'")
        if not all(isinstance(item, ObjectId) for item in value):
            raise TypeError(f"Property type inside list must be 'ObjectId'")
        if len(value) != len(list(DB['Chat'].find({"_id": {"$in": value}}))):
            # if len(value) != len([chats_collection.find_one({"_id": item}) for item in value]):
            raise ValidationError("Not all items found")
        self.__chats = value

    def chats_list(self):
        chats_collection = DB['Chat']
        # return [chats_collection.find_one({"_id": item} for item in self.items)]
        # return chats_collection.find({"_id": {"$in": self.__chats}})
        return [Chat(**document) for document in chats_collection.find({"_id": {"$in": self.__chats}})]

    @classmethod
    def all(cls):
        return [cls(**document) for document in cls.__collection.find()]

    @classmethod
    def find_one(cls, filter_):
        document = cls.__collection.find_one(filter=filter_)
        if document is None:
            return None
        return cls(document)

    @classmethod
    def find(cls, filter_):
        return cls.__collection.find(filter=filter_)
    # def all(self):
    #     return self.__collection.find()
    #
    # def find(self, filter_):
    #     return self.__collection.find(filter=filter_)


class Auction:

    def __init__(self, name, start_bid, bid_user=None, deadline=None):
        self.name = name
        self.start_bid = start_bid
        self.__bid = start_bid
        self.bid_user = bid_user
        self.deadline = deadline
        # dictionary = {key.replace('_Auction__', ''): self.__dict__[key] for key in self.__dict__}
        # self.__id = self.__users.insert_one(dictionary).inserted_id

    def get_vars(self):
        return {key.replace('_Auction__', ''): self.__dict__[key] for key in self.__dict__}

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError(f"Property type must be 'str', not '{type(value).__name__}'")
        self.__name = value

    @property
    def start_bid(self):
        return self.__start_bid

    @start_bid.setter
    def start_bid(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError(f"Property type must be 'int' or 'float', not '{type(value).__name__}'")
        if value < 0:
            raise ValidationError('Not negative value')
        self.__start_bid = value

    @property
    def bid(self):
        return self.__bid

    @bid.setter
    def bid(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError(f"Property type must be 'int' or 'float', not '{type(value).__name__}'")
        if value <= self.__bid:
            raise ValidationError('Not lower than current bid')
        self.__start_bid = value

    @property
    def bid_user(self):
        return self.__bid_user

    @bid_user.setter
    def bid_user(self, value):
        if not isinstance(value, ObjectId):
            raise TypeError(f"Property type must be 'ObjectId', not '{type(value).__name__}'")
        if not DB['User'].find_one(value):
            raise ValidationError(f"User with id of '{value.__id}' not found")
        self.__bid_user = value

    @property
    def deadline(self):
        return self.__deadline

    @deadline.setter
    def deadline(self, value):
        if not isinstance(value, datetime):
            raise TypeError(f"Property type must be 'datetime', not '{type(value).__name__}'")
        if value <= datetime.utcnow():
            raise ValidationError('Deadline cannot be put in the past')
        self.__deadline = value


class Item:
    __collection = DB['Item']

    def __init__(self, name, description, owner, image='images/items/default.jpg', auction=None):
        self.name = name
        self.description = description
        self.owner = owner
        self.image = image
        self.auction = auction
        # print(vars(self))
        dictionary = self.get_vars()
        document = self.__collection.find_one(dictionary)
        if not document:
            self.__id = self.__collection.insert_one(dictionary).inserted_id
        else:
            for key in document:
                setattr(self, key, document[key])

    def save(self):
        dictionary = self.get_vars()
        return self.__collection.update_one(filter={"_id": self.__id}, update=dictionary)

    def delete(self):
        return self.__collection.delete_one(filter={"_id": self.__id})

    def get_vars(self):
        dictionary = {key.replace('_Item__', ''): self.__dict__[key] for key in self.__dict__}
        dictionary['auction'] = self.auction.get_vars() if self.auction else self.auction
        return dictionary

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError(f"Property type must be 'str', not '{type(value).__name__}'")
        self.__name = value

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        if not isinstance(value, str):
            raise TypeError(f"Property type must be 'str', not '{type(value).__name__}'")
        self.__description = value

    @property
    def owner(self):
        return self.__owner

    @owner.setter
    def owner(self, value):
        if not isinstance(value, ObjectId):
            raise TypeError(f"Property type must be 'ObjectId', not '{type(value).__name__}'")
        if not DB['User'].find_one(value):
            raise ValidationError(f"User with id of '{value.__id}' not found")
        self.__owner = value

    @property
    def image(self):
        return self.__image

    @image.setter
    def image(self, value):
        file_storage = FileSystemStorage()
        if isinstance(value, str):
            if not file_storage.exists(value):
                raise ValidationError('File does not exist in a storage')
            filename = value
        elif isinstance(value, InMemoryUploadedFile):
            image = Image.open(value)
            image.verify()
            filename = f'images/items/{hash_file(value)}.{value.content_type.split("/")[-1]}'
            if not file_storage.exists(filename):
                file_storage.save(filename, value)
        else:
            raise TypeError(f"Property type must be 'str' or 'InMemoryUploadedFile', not '{type(value).__name__}'")

        # if not isinstance(value, str):
        #     raise TypeError(f"Property type must be a number, not '{type(value).__name__}'")
        self.__image = filename

    @property
    def auction(self):
        return self.__auction

    @auction.setter
    def auction(self, value):
        if not isinstance(value, Auction):
            raise TypeError(f"Property type must be 'Auction', not '{type(value).__name__}'")
        self.__auction = value

    @classmethod
    def all(cls):
        return [cls(**document) for document in cls.__collection.find()]

    @classmethod
    def find_one(cls, filter_):
        return cls(**cls.__collection.find_one(filter=filter_))

    @classmethod
    def find(cls, filter_):
        return cls.__collection.find(filter=filter_)


class Chat:
    __collection = DB['Chat']

    def __init__(self, document):
        self.__user1 = document['user1']
        self.__user2 = document['user2']
        self.__messages = document['messages'] if 'messages' in document else []
        self.__id = document['_id']

    def save(self):
        dictionary = self.get_vars()
        return self.__collection.update_one(filter={"_id": self.__id}, update=dictionary)

    def delete(self):
        return self.__collection.delete_one(filter={"_id": self.__id})

    def get_vars(self):
        dictionary = {key.replace('_Chat__', ''): self.__dict__[key] for key in self.__dict__}
        dictionary['messages'] = [message.get_vars() for message in self.__messages]
        return dictionary

    @property
    def id(self):
        return self.__id

    @property
    def user1(self):
        return User.find_one({'_id':self.__user1})

    @user1.setter
    def user1(self, value):
        if not isinstance(value, User):
            raise TypeError(f"Property type must be 'User', not '{type(value).__name__}'")
        if value == self.user2:
            raise ValueError(f"Value of property must be not value of value oter user")
        self.__user1 = value

    @property
    def user2(self):
        return User.find_one({'_id': self.__user2})

    @user2.setter
    def user2(self, value):
        if not isinstance(value, User):
            raise TypeError(f"Property type must be 'User', not '{type(value).__name__}'")
        if value == self.user1:
            raise ValueError(f"Value of property must be not value of value oter user")
        self.__user2 = value

    @property
    def messages(self):
        return self.__messages

    @messages.setter
    def messages(self, value):
        if not isinstance(value, list):
            raise TypeError(f"Property type must be a list of 'ObjectId', not '{type(value).__name__}'")
        if not all(isinstance(item, ObjectId) for item in value):
            raise TypeError(f"Property type inside list must be 'ObjectId'")
        if len(value) != len(list(DB['Message'].find({"id", {"$in": value}}))):
            raise ValidationError(f"Not all messages found")
        self.__messages = value

    def messages_list(self):
        return [Message(**document) for document in DB['Message'].find({"id", {"$in": self.__messages}})]

    @classmethod
    def all(cls):
        return [cls(**document) for document in cls.__collection.find()]

    @classmethod
    def find_one(cls, filter_):
        document = cls.__collection.find_one(filter=filter_)
        if document is None:
            return None
        return cls(document)

    @classmethod
    def find(cls, filter_):
        return cls.__collection.find(filter=filter_)

class Message:
    __collection = DB['Message']

    def __init__(self, text, user, image=None, url=None):
        self.text = text
        self.user = user
        self.__time = datetime.utcnow()
        dictionary = self.get_vars()
        document = self.__collection.find_one(dictionary)
        if not document:
            self.__id = self.__collection.insert_one(dictionary).inserted_id
        else:
            for key in document:
                setattr(self, key, document[key])
        # self.__id = self.__collection.insert_one(dictionary).inserted_id

    def save(self):
        dictionary = self.get_vars()
        return self.__collection.update_one(filter={"_id": self.__id}, update=dictionary)

    def delete(self):
        return self.__collection.delete_one(filter={"_id": self.__id})

    def get_vars(self):
        dictionary = {key.replace('_Message__', ''): self.__dict__[key] for key in self.__dict__}
        return dictionary

    @property
    def id(self):
        return self.__id

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value):
        if not isinstance(value, str):
            raise TypeError(f"Property type must be 'str', not '{type(value).__name__}'")
        self.__text = value

    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, value):
        if not isinstance(value, ObjectId):
            raise TypeError(f"Property type must be 'ObjectId', not '{type(value).__name__}'")
        if not DB['User'].find_one(value):
            raise ValidationError(f"User with id of '{value.__id}' not found")
        self.__user = value

    @property
    def time(self):
        return self.__time

    @time.setter
    def time(self, value):
        if not isinstance(value, datetime):
            raise TypeError(f"Property type must be 'datetime', not '{type(value).__name__}'")
        if value <= datetime.utcnow():
            raise ValidationError('Deadline cannot be put in the past')
        self.__time = value

    @classmethod
    def all(cls):
        return [cls(**document) for document in cls.__collection.find()]

    @classmethod
    def find_one(cls, filter_):
        return cls(**cls.__collection.find_one(filter=filter_))

    @classmethod
    def find(cls, filter_):
        return cls.__collection.find(filter=filter_)

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
