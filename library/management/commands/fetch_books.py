from django.core.management.base import BaseCommand
from library.models.book import Book
from library.models.author import Author
from library.models.publisher import Publisher
from library.models.genre import Genre
from library.models.tags import Tag
import random
from faker import Faker
from datetime import date

fake = Faker()


class Command(BaseCommand):
    help = 'Generate books'

    def handle(self, *args, **options):
        authors = Author.objects.all()
        publishers = list(Publisher.objects.all())
        genres = list(Genre.objects.all())
        tags = list(Tag.objects.all())

        for _ in range(500):  # Generate 500 books
            author = random.choice(authors)
            book_title = fake.catch_phrase()  # Generate a fake book title
            publisher = random.choice(publishers)
            genre = random.choice(genres)
            book_tags = random.sample(tags, 3)
            published_date = date(random.randint(1950, 2022), 1, 1)  # Generate a random published date
            stock_quantity = random.randint(5, 20)  # Generate a random quantity between 5 and 20
            book = Book.objects.create(title=book_title, author=author, publisher=publisher, published_date=published_date, stock_quantity=stock_quantity)
            book.genre.add(genre)
            book.tags.set(book_tags)
            book.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully created book {book_title}'))