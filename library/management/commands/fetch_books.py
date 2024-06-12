from django.core.management.base import BaseCommand
from library.models.book import Book
from library.models.author import Author
from library.models.publisher import Publisher
from library.models.genre import Genre
from library.models.tags import Tag
import random
from faker import Faker
from datetime import date
import requests
from django.core.files import File
from tempfile import NamedTemporaryFile

fake = Faker()

class Command(BaseCommand):
    help = 'Generate books with random covers'

    def handle(self, *args, **options):
        authors = Author.objects.all()
        publishers = list(Publisher.objects.all())
        genres = list(Genre.objects.all())
        tags = list(Tag.objects.all())

        for _ in range(100):  # Generate 100 books
            author = random.choice(authors)
            book_title = fake.catch_phrase()  # Generate a fake book title
            publisher = random.choice(publishers)
            genre = random.choice(genres)
            book_tags = random.sample(tags, 3)
            published_date = date(random.randint(1950, 2022), 1, 1)  # Generate a random published date
            stock_quantity = random.randint(5, 20)  # Generate a random quantity between 5 and 20

            book = Book.objects.create(
                title=book_title,
                author=author,
                publisher=publisher,
                published_date=published_date,
                stock_quantity=stock_quantity,
            )

            # Assign genre and tags
            book.genre.add(genre)
            book.tags.set(book_tags)

            # Fetch a random image from Lorem Picsum
            image_url = 'https://picsum.photos/200/300'
            response = requests.get(image_url)
            if response.status_code == 200:
                img_temp = NamedTemporaryFile(delete=True)
                img_temp.write(response.content)
                img_temp.flush()

                # Save the image to the book cover field
                book.cover.save(f'cover_{book.id}.jpg', File(img_temp), save=True)
                img_temp.close()

            self.stdout.write(self.style.SUCCESS(f'Successfully created book {book_title} with a random cover'))
