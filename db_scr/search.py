from models import Quote, Author
from connect import cache


def main():
    while True:

        text = input('Enter search target: ')
        if text.startswith('exit'):
            exit('Bye')

        field, data = parse_text(text)

        quotes = request_mongo(field, data)

        if quotes:
            quotes = list(rec.quote for rec in quotes)
            show_results(quotes)
        else:
            print('I cant find something with your request.')


@cache
def request_mongo(field: str, data: str):
    match field:

        case 'name':
            author = Author.objects(fullname=data).first()
            try:
                quotes = Quote.objects(author=author.id)
            except AttributeError:
                quotes = []
                print(f'I cant find author {data}')

        case 'tag':
            quotes = Quote.objects(tags__contains=data)

        case 'tags':
            tags = data.split(',')
            quotes = Quote.objects(tags__all=tags)

        case _:
            quotes = []

    return quotes


def parse_text(text):
    new_text = text.split(':')
    try:
        return new_text[0], new_text[1]
    except IndexError:
        return 'None', 'None'


def show_results(quotes):
    for rec in quotes:
        print(rec)


if __name__ == '__main__':
    main()
