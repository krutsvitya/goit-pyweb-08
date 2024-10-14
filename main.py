import json
from models import Author, Quote, Contact

with open('authors.json', 'r', encoding='utf-8') as f:
    authors_data = json.load(f)

for author in authors_data:
    if not Author.objects(fullname=author['fullname']).first():
        new_author = Author(
            fullname=author['fullname'],
            born_date=author.get('born_date'),
            born_location=author.get('born_location'),
            description=author.get('description')
        )
        new_author.save()

with open('qoutes.json', 'r', encoding='utf-8') as f:
    quotes_data = json.load(f)

for quote in quotes_data:
    author = Author.objects(fullname=quote['author']).first()
    if author and not Quote.objects(quote=quote['quote'], author=author).first():
        new_quote = Quote(
            tags=quote['tags'],
            author=author,
            quote=quote['quote']
        )
        new_quote.save()

while True:
    command = input("Введите команду: ").strip()
    if command == "exit":
        break

    if command.startswith("name:"):
        name = command[len("name:"):].strip()
        author = Author.objects(fullname=name).first()
        if author:
            quotes = Quote.objects(author=author)
            for q in quotes:
                print(q.quote.encode('utf-8').decode('utf-8'))
        else:
            print(f"Автор {name} не найден.")

    elif command.startswith("tag:"):
        tag = command[len("tag:"):].strip()
        quotes = Quote.objects(tags=tag)
        for q in quotes:
            print(q.quote.encode('utf-8').decode('utf-8'))

    elif command.startswith("tags:"):
        tags = command[len("tags:"):].strip().split(',')
        quotes = Quote.objects(tags__in=tags)
        for q in quotes:
            print(q.quote.encode('utf-8').decode('utf-8'))

