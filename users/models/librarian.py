from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class Librarian(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='librarian', verbose_name=_('User'))
    first_name = models.CharField(max_length=100, verbose_name=_('First Name'))
    last_name = models.CharField(max_length=100, verbose_name=_('Last Name'))
    personal_identification_number = models.CharField(max_length=20, unique=True,
                                                      verbose_name=_('Personal Identification Number'))
    salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Salary'))
    experience = models.PositiveIntegerField(verbose_name=_('Experience'), default=0)
    date_of_birth = models.DateField(verbose_name=_('Date of Birth'))
    address = models.TextField(verbose_name=_('Address'))
    phone_number = models.CharField(max_length=20, verbose_name=_('Phone Number'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    class Meta:
        verbose_name = _('Librarian')
        verbose_name_plural = _('Librarians')

    def __str__(self):
        return self.user.get_full_name()
