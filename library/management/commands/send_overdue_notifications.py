# library/management/commands/send_email_notifications.py
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from library.models import ReserveBook


class Command(BaseCommand):
    help = 'Send email notifications for canceled reservations'

    def handle(self, *args, **kwargs):
        canceled_reservations = ReserveBook.objects.filter(status='canceled')
        for reservation in canceled_reservations:
            self.send_cancellation_notification(reservation)

    def send_cancellation_notification(self, reservation):
        subject = 'Reservation Canceled Due to Overdue'
        message = f"Dear {reservation.user.first_name},\n\nYour reservation for the book '{reservation.book.title}' has been canceled due to overdue. Please make a new reservation if you still need the book.\n\nRegards,\nThe Library Team"
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [reservation.user.user.email],
            fail_silently=False,
        )
        self.stdout.write(self.style.SUCCESS(f'Sent cancellation notification to {reservation.user.username}'))
