from random import randint

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

User.add_to_class('enable_2fa', models.BooleanField(default=False))


def generate_reserve_key():
    """Hashed 12 digit key"""
    return randint(100000000000, 999999999999)


class Google2FA(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='google_2fa')
    reserve_key = models.CharField(max_length=12, default=generate_reserve_key)
    secret = models.CharField(max_length=16)

