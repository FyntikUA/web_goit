from models import Author, Quote

def search_by_tag(tag):
    quotes = Quote.objects(tags=tag)
    print_quotes(quotes)

def search_by_author(name):
    author = Author.objects(fullname=name).first()
    if author:
        quotes = Quote.objects(author=author)
        print_quotes(quotes)
    else:
        print("Автор не знайдений")

def search_by_tags(tags):
    tags_list = tags.split(',')
    quotes = Quote.objects(tags__in=tags_list)
    print_quotes(quotes)

def print_quotes(quotes):
    for quote in quotes:
        print(quote.quote)
        print("Автор:", quote.author.fullname)
        print("Теги:", ', '.join(quote.tags))
        print()
