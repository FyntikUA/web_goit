from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from mongoengine import Document, StringField, ListField, ReferenceField, DateTimeField, connect

uri = "mongodb+srv://FyntikUA:***********@cluster0.av2rj1b.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"


connect(host=uri, db='db_goit')


class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = DateTimeField()
    born_location = StringField()
    description = StringField()

class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author)
    quote = StringField()
