from random import randint

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from google_2fa.utils import make_reserve_key

User = get_user_model()

User.add_to_class('enable_2fa', models.BooleanField(default=False))


def generate_reserve_key() -> str:
    return str(randint(100000000000, 999999999999))


class Google2FA(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='two_fa')
    reserve_key = models.CharField(max_length=200, default=generate_reserve_key)
    secret = models.CharField(max_length=16)

    class Meta:
        verbose_name = _('Two Factor Authentication')
        verbose_name_plural = _('Two Factor Authentications')

    def __str__(self) -> str:
        return f'{self.user} 2FA'

    def set_reserve_key(self, reserve_key: str) -> None:
        self.reserve_key = make_reserve_key(reserve_key)
        self._reserve_key = reserve_key
