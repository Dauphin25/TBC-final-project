from django.db import models
from django.utils.translation import gettext_lazy as _
from library.choices import COUNTRY_CHOICES


class Author(models.Model):
    first_name = models.CharField(max_length=50, verbose_name=_('First Name'))
    last_name = models.CharField(max_length=50, verbose_name=_('Last Name'))
    country = models.CharField(max_length=50, verbose_name=_('Country'), choices=COUNTRY_CHOICES)
    birth_date = models.DateField(verbose_name=_('Birth Date'), default='1800-01-01')  # Default to a distant past date
    death_date = models.DateField(verbose_name=_('Death Date'), blank=True, null=True)
    biography = models.TextField(verbose_name=_('Biography'))

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
