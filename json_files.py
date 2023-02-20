from models import Author, Quote
import json
from connect import connect


def load_authors_from_file():
    with open('json_files/authors.json', 'r') as file:
        data = json.load(file)

    for record in data:
        author = Author(fullname=record['fullname'],
                        born_date=record['born_date'],
                        born_location=record['born_location'],
                        description=record['description'])
        author.save()

def load_quotes_from_file():
    with open('json_files/quotes.json', 'r') as file:
        data = json.load(file)

    for record in data:
        author = Author.objects(fullname=record['author']).first()

        try:
            quote = Quote(tags=record['tags'],
                           author=author.id,
                           quote=record['quote'])
            quote.save()
        except:
            print(f'I cant find author "{record["author"]}"')



if __name__ == '__main__':
    load_quotes_from_file()