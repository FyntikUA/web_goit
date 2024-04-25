import json
from datetime import datetime
from _models import Author, Quote

def load_authors_from_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        authors_data = json.load(file)
        for author_data in authors_data:
            author = Author(
                fullname=author_data['fullname'],
                born_date=datetime.strptime(author_data['born_date'], '%B %d, %Y'),
                born_location=author_data['born_location'],
                description=author_data['description']
            )
            author.save()

def load_quotes_from_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        quotes_data = json.load(file)
        for quote_data in quotes_data:
            author = Author.objects(fullname=quote_data['author']).first()
            if author:
                quote = Quote(
                    tags=quote_data['tags'],
                    author=author,
                    quote=quote_data['quote']
                )
                quote.save()

# Завантаження даних з файлів JSON у базу даних
load_authors_from_json('authors.json')
load_quotes_from_json('quotes.json')
