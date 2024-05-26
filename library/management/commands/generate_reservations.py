from django.core.management.base import BaseCommand
from users.models.library_user import LibraryUser
from library.models.reserve_book import ReserveBook
from library.models.book import Book
from faker import Faker
import random

fake = Faker()


class Command(BaseCommand):
    help = 'Generate random ReserveBook objects'

    def handle(self, *args, **options):
        for _ in range(100):  # Generate 100 ReserveBook objects
            # Get a random user and book
            user = random.choice(LibraryUser.objects.all())
            book = random.choice(Book.objects.filter(currently_available_quantity__gt=0))

            # Generate random data for the other fields
            take_date = fake.date_between(start_date='-14d', end_date='+14d')
            due_date = fake.date_between(start_date='+15d', end_date='+30d')
            is_taken = fake.boolean()
            status = random.choice(['active', 'canceled'])

            # Create the ReserveBook object
            reserve_book = ReserveBook(
                user=user,
                book=book,
                take_date=take_date,
                due_date=due_date,
                is_taken=is_taken,
                status=status,
            )
            reserve_book.save()

            self.stdout.write(self.style.SUCCESS(f'Successfully created ReserveBook object {reserve_book.id}'))