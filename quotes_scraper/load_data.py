import json
import mongoengine as me
from models import Author, Quote

me.connect(host="mongodb+srv://krutsvitya:vitya091003@krutsvitya.plhxk.mongodb.net/test?retryWrites=true&w=majority"
                "&appName=krutsvitya")


def load_authors(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        authors_data = json.load(file)
        for author in authors_data:
            existing_author = Author.objects(fullname=author['name']).first()
            if not existing_author:
                new_author = Author(
                    fullname=author['name'],
                    born_date=author['birthdate'],
                    born_location=author['birthplace'],
                    description=author['description']
                )
                new_author.save()


def load_quotes(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        quotes_data = json.load(file)
        for quote in quotes_data:
            author = Author.objects(fullname=quote['author']).first()
            if author:
                new_quote = Quote(
                    tags=quote['keywords'],
                    author=author,
                    quote=quote['quote']
                )
                new_quote.save()


load_authors('authors.json')
load_quotes('quotes.json')
