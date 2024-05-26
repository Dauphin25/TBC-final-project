# library/management/commands/create_publishers.py
from django.core.management.base import BaseCommand
from library.models.publisher import Publisher

class Command(BaseCommand):
    help = 'Create publishers'

    def handle(self, *args, **kwargs):
        publishers = [
    {
        'name': 'Gotham Press',
        'country': 'USA',
        'city': 'Gotham',
        'email': 'info@gothampress.com',
        'website': 'http://www.gothampress.com',
    },
    {
        'name': 'Hogwarts Publishing',
        'country': 'UK',
        'city': 'Hogsmeade',
        'email': 'info@hogwartspublishing.com',
        'website': 'http://www.hogwartspublishing.com',
    },
    {
        'name': 'Middle Earth Publications',
        'country': 'New Zealand',
        'city': 'Wellington',
        'email': 'info@middleearthpublications.com',
        'website': 'http://www.middleearthpublications.com',
    },
    {
        'name': 'Narnia Books',
        'country': 'UK',
        'city': 'London',
        'email': 'info@narniabooks.com',
        'website': 'http://www.narniabooks.com',
    },
    {
        'name': 'Panem Press',
        'country': 'USA',
        'city': 'Capitol',
        'email': 'info@panempress.com',
        'website': 'http://www.panempress.com',
    },
    {
        'name': 'Stark Industries Publishing',
        'country': 'USA',
        'city': 'New York',
        'email': 'info@starkindustriespublishing.com',
        'website': 'http://www.starkindustriespublishing.com',
    },
    {
        'name': 'Westeros Publications',
        'country': 'UK',
        'city': 'Belfast',
        'email': 'info@westerospublications.com',
        'website': 'http://www.westerospublications.com',
    },
    {
        'name': 'Dune Publishing',
        'country': 'USA',
        'city': 'Arrakis',
        'email': 'info@dunepublishing.com',
        'website': 'http://www.dunepublishing.com',
    },
    {
        'name': 'Matrix Media',
        'country': 'USA',
        'city': 'Zion',
        'email': 'info@matrixmedia.com',
        'website': 'http://www.matrixmedia.com',
    },
    {
        'name': 'Inception Ink',
        'country': 'USA',
        'city': 'Los Angeles',
        'email': 'info@inceptionink.com',
        'website': 'http://www.inceptionink.com',
    },
]

        for publisher_data in publishers:
            Publisher.objects.get_or_create(**publisher_data)
            self.stdout.write(self.style.SUCCESS(f'Successfully created publisher "{publisher_data["name"]}"'))