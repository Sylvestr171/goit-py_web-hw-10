import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hw10.settings")
django.setup()

from quotes.models import Author, Quote, Tag
from pymongo import MongoClient

from dotenv import load_dotenv
import urllib.parse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
dotenv_path = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path)  # завантажує .env у os.environ

username = os.getenv("MONGO_USER")
raw_password = os.getenv("MONGO_PASS")
if raw_password is None:
    raise ValueError("MONGO_PASS is not set in environment variables")
password = urllib.parse.quote(raw_password)
domain = os.getenv("DOMAIN")
db_name = os.getenv("DB_NAME")

uri = f"mongodb+srv://{username}:{password}@{domain}/{db_name}?retryWrites=true&w=majority&appName=Cluster0"
# mongodb+srv://Mongo:<db_password>@cluster0.7n1r9ws.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
client=MongoClient(uri, ssl=True)
db=client[db_name]

authors=db.authors.find()
for author in authors:
    Author.objects.get_or_create(
        fullname=author["fullname"],
        born_date=author["born_date"],
        born_location=author["born_location"],
        description=author["description"]
        )

quotes=db.quotes.find()
tags=[]
for quote in quotes:
    for tag in quote['tags']:
        t, *_ = Tag.objects.get_or_create(name=tag)
        tags.append(t)
    exist_quote = bool(len(Quote.objects.filter(quote=quote["quote"])))
    if not exist_quote:
        author = db.authors.find_one({"_id":quote["author"]})
        a = Author.objects.get(fullname=author["fullname"])
        q = Quote.objects.create(
            quote = quote["quote"],
            author = a
            )
        for tag in tags:
            q.tags.add(tag)
