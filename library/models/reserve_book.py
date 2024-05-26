from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models.library_user import LibraryUser
from django.utils import timezone


class ReserveBook(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('canceled', 'Canceled'),
    ]
    book = models.ForeignKey('Book', on_delete=models.CASCADE, verbose_name=_('Book'))
    user = models.ForeignKey(LibraryUser, on_delete=models.CASCADE, verbose_name=_('User'))
    reserved_date = models.DateField(verbose_name=_('Reserved Date'), auto_now_add=True)
    take_date = models.DateField(verbose_name=_('Take Date'), null=True, blank=True, default=timezone.now)
    due_date = models.DateField(verbose_name=_('Due Date'))
    is_taken = models.BooleanField(default=False, verbose_name=_('Is Taken'))
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f'{self.book} - {self.user}'

    def save(self, *args, **kwargs):
        if self.pk is None and self.book.currently_available_quantity > 0:
            self.book.reserve_book()
        super().save(*args, **kwargs)

    def cancel(self):
        self.status = 'canceled'
        self.book.cancel_reservation()
        self.save()