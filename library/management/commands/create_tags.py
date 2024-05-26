# library/management/commands/create_tags.py
from django.core.management.base import BaseCommand
from library.models.tags import Tag


class Command(BaseCommand):
    help = 'Create tags'

    def handle(self, *args, **kwargs):
        tags = [
            'Best Seller',
            'Classic',
            'New Release',
            'Staff Picks',
            'Award Winning',
            'Based on True Story',
            'Young Adult',
            'Children',
            'Adult',
            'Contemporary',
            'Historical',
            'Fiction',
            'Non-Fiction',
            'Fantasy',
            'Sci-Fi',
            'Mystery',
            'Thriller',
            'Horror',
            'Romance',
            'Adventure',
            'Biography',
            'Autobiography',
            'Self-Help',
            'Educational',
            'Graphic Novel',
            'Comic',
            'Dystopian',
            'Paranormal',
            'Action',
            'Humor'
        ]
        for tag_name in tags:
            Tag.objects.get_or_create(name=tag_name)
            self.stdout.write(self.style.SUCCESS(f'Successfully created tag "{tag_name}"'))