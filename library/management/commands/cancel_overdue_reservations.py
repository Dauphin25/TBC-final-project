from django.core.management.base import BaseCommand
from django.utils import timezone
from library.models import ReserveBook


class Command(BaseCommand):
    help = 'Cancel overdue reservations'

    def handle(self, *args, **kwargs):
        overdue_reservations = ReserveBook.objects.filter(due_date__lt=timezone.now(), status='active')
        for reservation in overdue_reservations:
            reservation.status = 'canceled'
            reservation.save()
        self.stdout.write(self.style.SUCCESS(f'Canceled {overdue_reservations.count()} overdue reservations'))
