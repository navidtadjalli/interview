from django.db import models
from django.utils.translation import gettext_lazy as _


class Customer(models.Model):
    phone_number = models.CharField(
        verbose_name=_('Phone Number'),
        max_length=11,
        null=False,
        blank=False
    )
    first_name = models.CharField(
        verbose_name=_('First Name'),
        max_length=20,
        null=False,
        blank=False
    )
    last_name = models.CharField(
        verbose_name=_('Last Name'),
        max_length=50,
        null=False,
        blank=False
    )
    email = models.EmailField(
        verbose_name=_('E-mail'),
        null=False,
        blank=False
    )
    registered_at = models.DateTimeField(
        verbose_name=_('Registered at'),
        auto_now_add=True,
        editable=False
    )
    last_login_at = models.DateTimeField(
        verbose_name=_('Last Login at'),
        editable=False,
        null=True
    )

    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')
        ordering = ('last_name', 'first_name')

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"
