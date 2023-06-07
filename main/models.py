import datetime
from functools import partial

from bson import ObjectId
from AuctionProject.settings import MEDIA_URL
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

CLIENT = MongoClient(settings.DATABASES['default']['CONNECTION'])
DB = CLIENT[settings.DATABASES['default']['NAME']]


def hash_file(file, block_size=65536):
    hasher = hashlib.sha256()
    for buf in iter(partial(file.read, block_size), b''):
        hasher.update(buf)
    return hasher.hexdigest()


class User:
    __collection = DB['User']
    # __items = DB['Item']
    # __chats = DB['Chat']
    __roles = ('admin', 'mod', 'user', 'guest')

    def __init__(self, _id, name, password, email, balance=0, role='user',
                 image='images/users/default.png', chats=[]):  # , items=[]):
        self.__id = _id
        self.__name = name
        self.__password = password
        self.__email = email
        self.__balance = balance
        self.__role = role
        self.__image = image
        # self.online = False
        # self.__items = items
        self.__chats = chats

    def save(self):
        # dictionary = self.get_vars()  # {key.replace('_User__', ''): self.__dict__[key] for key in self.__dict__}
        # dictionary.pop('id')
        return self.__collection.update_one(filter={"_id": self.__id}, update={'$set': self.get_vars()})

    @classmethod
    def update(cls, obj):
        return cls.__collection.update_one({"_id": obj.__id}, obj.get_vars())

    def delete(self):
        return self.__collection.delete_one(filter={"_id": self.__id})

    def get_vars(self):
        dictionary = {key.replace('_User__', ''): self.__dict__[key] for key in self.__dict__}
        dictionary.pop('id')
        return dictionary

    def try_login(self, password):
        return make_password(password) == self.password

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        if not isinstance(value, ObjectId):
            raise TypeError(f"Property type must be 'ObjectId', not '{type(value).__name__}'")
        # if not self.__collection.find_one({"_id": value}):
        #     raise ValidationError(f"Object with Id of {value} not found")
        self.__id = value

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
        self.__password = make_password(value)
        self.save()

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        if not isinstance(value, str):
            raise TypeError(f"Property type must be 'str', not '{type(value).__name__}'")
        validate_email(value)
        self.__email = value
        self.save()

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
            filename = MEDIA_URL + "/" + filename
        else:
            raise TypeError(f"Property type must be 'str' or 'InMemoryUploadedFile', not '{type(value).__name__}'")
        self.__image = filename
        self.save()

    # @property
    # def online(self):
    #     return self.__online is None

    # @online.setter
    # def online(self, value):
    #     if not isinstance(value, bool):
    #         raise TypeError(f"Property type must be 'bool', not '{type(value).__name__}'")
    #     self.__online = None if value else datetime.utcnow()
    # @property
    # def items(self):
    #     return self.__items
    #
    # def items_list(self):
    #     return [Item(**document) for document in DB['Item'].find({"_id": {"$in": self.__items}})]
    #
    # @items.setter
    # def items(self, value):
    #     if not isinstance(value, list):
    #         raise TypeError(f"Property type must be a list of 'ObjectId', not '{type(value).__name__}'")
    #     if not all(isinstance(item, ObjectId) for item in value):
    #         raise TypeError(f"Property type inside list must be 'ObjectId'")
    #     if len(value) != len(list(DB['Item'].find({"_id": {"$in": value}}))):
    #         # items_collection = DB['Item']
    #         # if len(value) != len([items_collection.find_one({"_id": item}) for item in value]):
    #         raise ValidationError("Not all items found")
    #     self.__items = value

    @property
    def chats(self):
        return self.__chats

    @chats.setter
    def chats(self, value):
        if not isinstance(value, list):
            raise TypeError(f"Property type must be a list of 'ObjectId', not '{type(value).__name__}'")
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
    def find_one(cls, filter_=None):
        document = cls.__collection.find_one(filter=filter_)
        if document is None:
            return None
        document['_id'] = document.pop('_id')
        return cls(**document)

    @classmethod
    def find(cls, filter_):
        return cls.__collection.find(filter=filter_)

    @classmethod
    def create(cls, name, password, email, balance=0, role='user', image='images/users/default.png', chats=[]):
        #       items=[], chats=[]):
        # if not(User.find_one({'name': name}) is None):
        #     raise ValueError("акаунт з цим ім'ям вже існує")
        # if not(User.find_one({'email': email}) is None):
        #     raise ValueError("акаунт з цим емейлом вже існує")
        user = cls(None, name, password, email, balance, role, image, chats)  # , items
        user.id = cls.__collection.insert_one(user.get_vars()).inserted_id
        return user


class Auction:

    def __init__(self, start_bid, bid_user=None, deadline=None):  # , name
        # self.__name = name
        self.__start_bid = start_bid
        self.__bid = start_bid
        self.__bid_user = bid_user
        self.__deadline = deadline
        # dictionary = {key.replace('_Auction__', ''): self.__dict__[key] for key in self.__dict__}
        # self.__id = self.__users.insert_one(dictionary).inserted_id

    def get_vars(self):
        return {key.replace('_Auction__', ''): self.__dict__[key] for key in self.__dict__}

    # @property
    # def name(self):
    #     return self.__name
    #
    # @name.setter
    # def name(self, value):
    #     if not isinstance(value, str):
    #         raise TypeError(f"Property type must be 'str', not '{type(value).__name__}'")
    #     self.__name = value

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

    def __init__(self, _id, name, description, owner, image='images/items/default.jpg', auction=None):
        self.__id = _id
        self.__name = name
        self.__description = description
        self.__owner = owner
        self.__image = image
        self.__auction = auction
        # print(vars(self))
        # dictionary = self.get_vars()
        # document = self.__collection.find_one(dictionary)
        # if not document:
        #     self.__id = self.__collection.insert_one(dictionary).inserted_id
        # else:
        #     for key in document:
        #         setattr(self, key, document[key])

    def save(self):
        dictionary = self.get_vars()
        return self.__collection.update_one(filter={"_id": self.__id}, update=dictionary)

    @classmethod
    def update(cls, obj):
        return cls.__collection.update_one({"_id": obj.__id}, obj.get_vars())

    def delete(self):
        return self.__collection.delete_one(filter={"_id": self.__id})

    def get_vars(self):
        dictionary = {key.replace('_Item__', ''): self.__dict__[key] for key in self.__dict__}
        dictionary['auction'] = self.auction.get_vars() if self.auction else self.auction
        dictionary['owner'] = self.owner
        # dictionary.pop('id')
        return dictionary

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        if not isinstance(value, ObjectId):
            raise TypeError(f"Property type must be 'ObjectId', not '{type(value).__name__}'")
        # if not self.__collection.find_one({"_id": value}):
        #     raise ValidationError(f"Object with Id of {value} not found")
        self.__id = value

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

    def owner_user(self):
        return User.find_one({'_id': ObjectId(self.__owner)})

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
            filename = MEDIA_URL + filename
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
    def find_one(cls, filter_=None):
        document = cls.__collection.find_one(filter=filter_)
        if not document:
            return document
        document['_id'] = document.pop('_id')
        return cls(**document)

    @classmethod
    def find(cls, filter_):
        return cls.__collection.find(filter=filter_)

    @classmethod
    def create(cls, name, description, owner, image='images/items/default.jpg', auction=None):
        item = cls(None, name, description, owner, image, auction)
        item.id = cls.__collection.insert_one(item.get_vars()).inserted_id
        return item


class Chat:
    __collection = DB['Chat']

    def __init__(self, _id, user1, user2, messages=[]):
        self.user1 = user1
        self.user2 = user2
        # print(messages)
        self.messages = messages
        # print(self.messages)
        self.__id = _id

    def save(self):
        dictionary = self.get_vars()
        return self.__collection.update_one(filter={"_id": self.__id}, update={'$set': dictionary})

    @classmethod
    def update(cls, obj):
        return cls.__collection.update_one({"_id": obj.__id}, obj.get_vars())

    def delete(self):
        return self.__collection.delete_one(filter={"_id": self.__id})

    def get_vars(self):
        dictionary = {key.replace('_Chat__', ''): self.__dict__[key] for key in self.__dict__}
        print(dictionary)
        dictionary.pop('id')
        # dictionary['messages'] = [message.get_vars() for message in self.__messages]
        return dictionary

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        if not isinstance(value, ObjectId):
            raise TypeError(f"Property type must be 'ObjectId', not '{type(value).__name__}'")
        # if not self.__collection.find_one({"_id": value}):
        #     raise ValidationError(f"Object with Id of {value} not found")
        self.__id = value

    @property
    def user1(self):
        return User.find_one({'_id': self.__user1})

    @user1.setter
    def user1(self, value):
        if not isinstance(value, ObjectId):
            raise TypeError(f"Property type must be 'ObjectId', not '{type(value).__name__}'")
        if hasattr(self, '__user2') and value == self.__user2:
            raise ValueError(f"Value of property must be not value of value other user")
        self.__user1 = value

    @property
    def user2(self):
        return User.find_one({'_id': self.__user2})

    @user2.setter
    def user2(self, value):
        if not isinstance(value, ObjectId):
            raise TypeError(f"Property type must be 'ObjectId', not '{type(value).__name__}'")
        if value == self.__user1:
            raise ValueError(f"Value of property must be not value of value other user")
        self.__user2 = value

    @property
    def messages(self):
        # list_messages = [Message.find_one({'_id': ObjectId(message)}) for message in self.__messages]
        list_messages = []
        # message = None
        for _id in self.__messages:
            message = Message.find_one({'_id': ObjectId(_id)})
            if not message:
                self.__messages.remove(_id)
                self.save()
            list_messages.append(message)
        return list_messages

    @messages.setter
    def messages(self, value):
        if not isinstance(value, list):
            raise TypeError(f"Property type must be a list of 'ObjectId', not '{type(value).__name__}'")
        if not all(isinstance(item, ObjectId) for item in value):
            raise TypeError(f"Property type inside list must be 'ObjectId'")
        self.__messages = value

    # def messages_list(self):
    #     return [Message(**document) for document in DB['Message'].find({"id", {"$in": self.__messages}})]

    @classmethod
    def all(cls):
        return [cls(**document) for document in cls.__collection.find()]

    @classmethod
    def find_one(cls, filter_=None):
        document = cls.__collection.find_one(filter=filter_)
        if not document:
            return document
        document['_id'] = document.pop('_id')
        return cls(**document)

    @classmethod
    def find_one_by_users(cls, user1, user2):
        users = [ObjectId(user1.id), ObjectId(user2.id)]
        document = cls.__collection.find_one({'$and': [{'user1': {'$in': users}}, {'user2': {'$in': users}}]})
        if document is None:
            return None
        # print(document)
        # document['_id'] = document.pop('_id')
        return cls(**document)

    @classmethod
    def find(cls, filter_):
        return cls.__collection.find(filter=filter_)

    @classmethod
    def create(cls, user1, user2, messages=[]):
        chat = cls(None, user1.id, user2.id, messages)
        chat.id = chat.__collection.insert_one(chat.get_vars()).inserted_id
        return chat

    def send(self, message):
        self.__messages.append(message.id)
        Chat.__collection.update_one(filter={"_id": self.__id}, update={'$push': {'messages': ObjectId(message.id)}})


class Message:
    __collection = DB['Message']

    def __init__(self, _id, text, user, image=None, url=None, time=None):
        self.__id = id
        self.__text = text
        self.__user = user
        self.__time = time
        if self.__time is None:
            self.__time = datetime.utcnow()
        # dictionary = self.get_vars()
        # document = self.__collection.find_one(dictionary)
        # if not document:
        #     self.__id = self.__collection.insert_one(dictionary).inserted_id
        # else:
        #     for key in document:
        #         setattr(self, key, document[key])
        # self.__id = self.__collection.insert_one(dictionary).inserted_id

    def save(self):
        dictionary = self.get_vars()
        return self.__collection.update_one(filter={"_id": self.__id}, update=dictionary)

    @classmethod
    def update(cls, obj):
        return cls.__collection.update_one({"_id": obj.__id}, obj.get_vars())

    def delete(self):
        return self.__collection.delete_one(filter={"_id": self.__id})

    def get_vars(self):
        dictionary = {key.replace('_Message__', ''): self.__dict__[key] for key in self.__dict__}
        dictionary.pop('id')
        return dictionary

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        if not isinstance(value, ObjectId):
            raise TypeError(f"Property type must be 'ObjectId', not '{type(value).__name__}'")
        if not self.__collection.find_one({"_id": value}):
            raise ValidationError(f"Object with Id of {value} not found")
        self.__id = value

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value):
        if not isinstance(value, str):
            raise TypeError(f"Property type must be 'str', not '{type(value).__name__}'")
        if len(value) <= 0:
            raise ValidationError("Empty property 'text' is not allowed")
        self.__text = value

    @property
    def user(self):
        return User.find_one({'_id': self.__user})

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
    def find_one(cls, filter_=None):
        document = cls.__collection.find_one(filter=filter_)
        if not document:
            return document
        # document['id'] = document.pop('_id')
        return cls(**document)

    @classmethod
    def find(cls, filter_):
        return cls.__collection.find(filter=filter_)

    @classmethod
    def create(cls, text, user, image=None, url=None):
        message = cls(None, text, user, image, url)
        print(message.get_vars())
        message.id = cls.__collection.insert_one(message.get_vars()).inserted_id
        return message


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
