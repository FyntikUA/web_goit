
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from mongoengine import Document, StringField, ListField, ReferenceField, DateTimeField, connect



uri = "mongodb+srv://FyntikUA:cz35MKNbEpLU4zai@cluster0.av2rj1b.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client.db_goit

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


# Підключення до бази даних MongoDB
connect(host=uri, db='db_goit')
print('Conected to base.')

class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = DateTimeField()
    born_location = StringField()
    description = StringField()

class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author)
    quote = StringField()

# Функція для пошуку цитат за тегом
def search_by_tag(tag):
    quotes = Quote.objects(tags=tag)
    print_quotes(quotes)

# Функція для пошуку цитат за ім'ям автора
def search_by_author(name):
    author = Author.objects(fullname=name).first()
    if author:
        quotes = Quote.objects(author=author)
        print_quotes(quotes)
    else:
        print("Автор не знайдений")

# Функція для пошуку цитат за набором тегів
def search_by_tags(tags):
    tags_list = tags.split(',')
    quotes = Quote.objects(tags__in=tags_list)
    print_quotes(quotes)

# Допоміжна функція для виведення цитат
def print_quotes(quotes):
    for quote in quotes:
        print(quote.quote)
        print("Автор:", quote.author.fullname)
        print("Теги:", ', '.join(quote.tags))
        print()

# Основний цикл програми
while True:
    command = input("Введіть команду (наприклад, name: Steve Martin, tag:life, tags:life,live, або exit для виходу): ")
    if command.startswith("name:"):
        name = command.split("name:")[1].strip()
        search_by_author(name)
    elif command.startswith("tag:"):
        tag = command.split("tag:")[1].strip()
        search_by_tag(tag)
    elif command.startswith("tags:"):
        tags = command.split("tags:")[1].strip()
        search_by_tags(tags)
    elif command == "exit":
        break
    else:
        print("Невідома команда. Спробуйте ще раз.")