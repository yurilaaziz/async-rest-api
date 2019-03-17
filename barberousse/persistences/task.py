from mongoengine import *


class Task(Document):
    module = StringField(required=True)
    _id = StringField(required=True, primary_key=True)
    status = StringField(required=True)
    args = DictField(required=False)
    time_start = DateTimeField(required=True)
    time_finish = DateTimeField(required=False)
    time = FloatField(required=False)
    traceback = ListField(StringField())
    error = ListField(StringField())
