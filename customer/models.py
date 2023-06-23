from typing import Optional

from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CustomerManager(BaseUserManager):
    @classmethod
    def normalize_phone_number(cls, phone_number: str) -> str:
        phone_number = phone_number or ""
        phone_number = phone_number.replace(" ", "")

        return phone_number

    def _create_user(self, phone_number: str, password: str, **extra_fields):
        if not phone_number:
            raise ValueError("The given phone number must be set")
        phone_number: str = self.normalize_phone_number(phone_number)
        user: Customer = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number: str, password: Optional[str] = None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_staff", False)
        return self._create_user(phone_number, password, **extra_fields)

    def create_superuser(self, phone_number: str, password: Optional[str] = None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone_number, password, **extra_fields)


class Customer(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(
        verbose_name=_('Phone Number'),
        max_length=11,
        unique=True,
        null=False,
        blank=False
    )
    # Fields imported from Django's AbstractUser class
    first_name = models.CharField(
        verbose_name=_('First Name'),
        max_length=150,
        null=False,
        blank=False
    )
    last_name = models.CharField(
        verbose_name=_('Last Name'),
        max_length=150,
        null=False,
        blank=False
    )
    email = models.EmailField(
        verbose_name=_('E-mail'),
        null=False,
        blank=False
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    date_joined = models.DateTimeField(
        verbose_name=_("date joined"),
        default=timezone.now
    )
    # End

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    objects = CustomerManager()

    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')
        ordering = ('last_name', 'first_name')

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"
