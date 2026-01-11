from pymongo import MongoClient
from django.conf import settings

client = MongoClient(settings.MONGO_URI)
db = client['todo_db']
todos_collection = db['todos']
