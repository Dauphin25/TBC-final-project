import random
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from faker import Faker
from users.models.library_user import LibraryUser

fake = Faker()


class Command(BaseCommand):
    help = 'Generate users with random names, email addresses, and passwords'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Number of users to generate')

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        for i in range(1, count + 1):
            username = f'user{i}'
            email = f'{username}@gmail.com'
            password = f'{username}password'
            first_name = fake.first_name()
            last_name = fake.last_name()
            user = User.objects.create_user(username=username, email=email, password=password,
                                            first_name=first_name, last_name=last_name)
            library_user = LibraryUser.objects.create(user=user, first_name=first_name, last_name=last_name,
                                                      library_card_number=fake.unique.random_number(digits=10),
                                                      personal_identification_number=fake.unique.random_number(digits=10),
                                                      date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=100),
                                                      address=fake.address(), phone_number=fake.phone_number())
            self.stdout.write(self.style.SUCCESS(f'Successfully created user: {user.username}'))
