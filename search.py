import redis

from models import Quote, Author
from connect import connect, redis_connect


def main():
    while True:

        text = input('Enter search target: ').split(':')
        if text[0] == 'exit':
            break
        if len(text) < 2:
            print('Not enough information.')
            continue
        field, data = text[0], text[1]

        quotes = redis_connect.lrange(field+data, 0, -1)

        if quotes:
            print('Successfully from redis')
            quotes = list(rec.decode('utf-8') for rec in quotes)
            show_results(quotes)
            continue

        match field:
            case 'name':
                author = Author.objects(fullname=data).first()
                try:
                    quotes = Quote.objects(author=author.id)
                except AttributeError:
                    print(f'I cant find author {data}')
                    continue

            case 'tag':
                quotes = Quote.objects(tags__contains=data)

            case 'tags':
                tags = data.split(',')
                quotes = Quote.objects(tags__all=tags)

            case _:
                print(f'I dont know this command "{field}".')
                continue

        if quotes:
            quotes = list(rec.quote for rec in quotes)
            hash(field, data, quotes)
            show_results(quotes)
        else:
            print('I cant find something with your request.')


def hash(field, data, quotes):

    print(f'"successfully hashed"')
    redis_connect.rpush(field+data, *quotes)


def show_results(quotes):
    for rec in quotes:
        print(rec)


if __name__ == '__main__':
    main()
