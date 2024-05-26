from django.db import models
from django.utils.translation import gettext_lazy as _


class Publisher(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    country = models.CharField(max_length=50, verbose_name=_('Country'))
    city = models.CharField(max_length=50, verbose_name=_('City'))
    email = models.EmailField(verbose_name=_('Email'))
    website = models.URLField(verbose_name=_('Website'))

    def __str__(self):
        return self.name
