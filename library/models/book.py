from django.db import models
from django.utils.translation import gettext_lazy as _


class Book(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('Title'))
    author = models.ForeignKey('Author', on_delete=models.CASCADE, verbose_name=_('Author'))
    genre = models.ManyToManyField('Genre',  verbose_name=_('Genre'), blank=True)
    publisher = models.ForeignKey('Publisher', on_delete=models.CASCADE, verbose_name=_('Publisher'))
    published_date = models.DateField(verbose_name=_('Published Date'), blank=True, null=True)
    tags = models.ManyToManyField('Tag',  verbose_name=_('Tags'), blank=True)
    stock_quantity = models.IntegerField(verbose_name=_('Stock Quantity'))
    borrowed_quantity = models.IntegerField(verbose_name=_('Borrowed Quantity'), default=0)
    current_borrowed_quantity = models.IntegerField(verbose_name=_('Current Borrowed Quantity'), default=0)
    currently_available_quantity = models.IntegerField(verbose_name=_('Currently Available Quantity'), default=0)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.currently_available_quantity = self.stock_quantity - self.current_borrowed_quantity
        super().save(*args, **kwargs)

    def borrow_book(self):
        if self.currently_available_quantity > 0:
            self.current_borrowed_quantity += 1
            self.borrowed_quantity += 1
            self.currently_available_quantity -= 1
            self.save()

    def return_book(self):
        if self.current_borrowed_quantity > 0:
            self.current_borrowed_quantity -= 1
            self.save()

    def reserve_book(self):
        if self.currently_available_quantity > 0:
            self.currently_available_quantity -= 1
            self.save()

    def cancel_reservation(self):
        self.currently_available_quantity += 1
        self.save()
