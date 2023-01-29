from typing import TypeVar

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import UserManager

UserType = TypeVar('UserType', bound='User')


class User(AbstractUser):
    username = None  # type: ignore
    email = models.EmailField(_('Email address'), unique=True)

    USERNAME_FIELD: str = 'email'
    REQUIRED_FIELDS: list[str] = []

    objects = UserManager()  # type: ignore

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self) -> str:
        return self.email

    def full_name(self) -> str:
        return super().get_full_name()
