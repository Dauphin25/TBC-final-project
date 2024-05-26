# library/management/commands/create_genres.py
from django.core.management.base import BaseCommand
from library.models.genre import Genre


class Command(BaseCommand):
    help = 'Create genres'

    def handle(self, *args, **kwargs):
        genres = [
            'Action and Adventure',
            'Classics',
            'Comic Book or Graphic Novel',
            'Detective and Mystery',
            'Fantasy',
            'Historical Fiction',
            'Horror',
            'Literary Fiction',
            'Romance',
            'Science Fiction (Sci-Fi)',
            'Short Stories',
            'Suspense and Thrillers',
            'Biographies and Autobiographies',
            'Cookbooks',
            'Essay',
            'History',
            'Memoir',
            'Poetry',
            'Self-help / Personal',
            'Development',
            'True Crime',
            'Art',
            'Personal',
            'Development',
            'Philosophy',
            'Photography',
            'Religion',
            'Science',
            'Travel',
            'True Crime'
        ]
        for genre_name in genres:
            Genre.objects.get_or_create(name=genre_name)
            self.stdout.write(self.style.SUCCESS(f'Successfully created genre "{genre_name}"'))