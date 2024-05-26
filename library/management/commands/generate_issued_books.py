# library/management/commands/generate_issued_books.py
from django.core.management.base import BaseCommand
from library.models.issued_book import IssuedBook
from library.models.book import Book
from users.models.library_user import LibraryUser
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Generate 100 IssuedBook objects'

    def handle(self, *args, **options):
        books = list(Book.objects.all())
        users = list(LibraryUser.objects.all())

        if not books or not users:
            self.stdout.write(self.style.ERROR('No books or users found. Please make sure you have some books and users in your database.'))
            return

        for _ in range(100):
            book = random.choice(books)
            user = random.choice(users)
            issued_date = datetime.now() - timedelta(days=random.randint(1, 365))  # Random issue date in the past year
            due_date = issued_date + timedelta(days=random.randint(1, 30))  # Random due date within 30 days of issue
            returned = random.choice([True, False])  # Randomly decide if the book was returned

            if returned:
                return_date = due_date + timedelta(days=random.randint(1, 30))  # If returned, random return date within 30 days of due date
            else:
                return_date = None

            IssuedBook.objects.create(
                book=book,
                user=user,
                issued_date=issued_date,
                due_date=due_date,
                returned=returned,
                return_date=return_date
            )

        self.stdout.write(self.style.SUCCESS('Successfully created 100 IssuedBook objects'))