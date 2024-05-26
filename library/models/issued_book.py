# models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models.library_user import LibraryUser
from library.models.book import Book


class IssuedBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name=_('Book'))
    user = models.ForeignKey(LibraryUser, on_delete=models.CASCADE, verbose_name=_('User'))
    issued_date = models.DateField(verbose_name=_('Issued Date'))
    due_date = models.DateField(verbose_name=_('Due Date'))
    returned = models.BooleanField(default=False, verbose_name=_('Returned'))
    return_date = models.DateField(verbose_name=_('Return Date'), null=True, blank=True)

    class Meta:
        verbose_name = _('Issued Book')
        verbose_name_plural = _('Issued Books')

    def __str__(self):
        return f'{self.book.title} issued to {self.user.user.get_full_name()}'

    def mark_as_returned(self):
        if not self.returned:
            self.returned = True
            self.book.return_book()
            self.save()

