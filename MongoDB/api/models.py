from mongoengine import *
from datetime import datetime


# Create your models here.
class Article(DynamicDocument):
    title = StringField()
    author = StringField()
    mainCategory = StringField(null=False)
    subCategory = StringField(null=False)
    price = IntField(null=False)
    discount = FloatField()
    origin_price = IntField()
    publisher = StringField()
    descriptions = StringField(null=False)
    translator = StringField()
    language = StringField()
    published_date = DateTimeField()