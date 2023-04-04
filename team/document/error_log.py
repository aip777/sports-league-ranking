from mongoengine import *
import datetime
from mongoengine import *


class Error(Document):
    model = StringField(required=True, max_length=200)
    posted = DateTimeField(default=datetime.datetime.utcnow)
    tags = ListField(StringField(max_length=50))
    meta = {"allow_inheritance": True}


class ErrorLog(Error):
    message = StringField(required=True)


class LinkPost(Error):
    url = StringField(required=True)
