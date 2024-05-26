from django.core.management.base import BaseCommand
from library.models.book import Book
from library.models.author import Author
from library.models.publisher import Publisher
from library.models.genre import Genre
from library.models.tags import Tag
import wikipediaapi
import random


class Command(BaseCommand):
    help = 'Generate books'

    def handle(self, *args, **options):
        wiki_wiki = wikipediaapi.Wikipedia(
            language='en',
            user_agent='My Application (version 1.0, more info at mywebsite.com, contact at myemail@mywebsite.com)'
        )
        authors = Author.objects.all()
        publishers = list(Publisher.objects.all())
        genres = list(Genre.objects.all())
        tags = list(Tag.objects.all())

        for author in authors:
            page_py = wiki_wiki.page(author.first_name + ' ' + author.last_name)

            if page_py.exists():
                book_title = page_py.title
                publisher = random.choice(publishers)
                genre = random.choice(genres)
                book_tags = random.sample(tags, 3)
                book = Book.objects.create(title=book_title, author=author, publisher=publisher, stock_quantity=10)
                book.genre.add(genre)
                book.tags.set(book_tags)
                book.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully created book {book_title}'))
            else:
                self.stdout.write(self.style.WARNING(f'No Wikipedia page found for author {author.first_name} {author.last_name}'))