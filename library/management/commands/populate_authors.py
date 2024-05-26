from django.core.management.base import BaseCommand
from library.models.author import Author
from library.choices import authors


class Command(BaseCommand):
    help = 'Generate 30 authors'

    def handle(self, *args, **options):
        fake_authors = authors

        for author in fake_authors:
            Author.objects.create(**author)

        self.stdout.write(self.style.SUCCESS('Successfully created authors'))