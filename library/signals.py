from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import IssuedBook, ReserveBook


@receiver(post_save, sender=IssuedBook)
def update_book_on_issue(sender, instance, created, **kwargs):
    if created:
        book = instance.book
        book.borrow_book()


@receiver(post_delete, sender=IssuedBook)
def update_book_on_return(sender, instance, **kwargs):
    book = instance.book
    book.return_book()


@receiver(post_save, sender=ReserveBook)
def update_book_on_reserve(sender, instance, created, **kwargs):
    if created and instance.status == 'active':
        book = instance.book
        book.reserve_book()


@receiver(post_delete, sender=ReserveBook)
def update_book_on_cancel(sender, instance, **kwargs):
    if instance.status == 'active':
        book = instance.book
        book.cancel_reservation()


@receiver(post_save, sender=IssuedBook)
def update_book_on_return(sender, instance, **kwargs):
    if instance.returned:
        instance.book.return_book()


@receiver(post_save, sender=ReserveBook)
def update_book_on_take(sender, instance, **kwargs):
    if instance.is_taken:
        instance.book.borrow_book()
