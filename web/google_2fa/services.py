from typing import Optional

import requests
from django.contrib.auth import get_user_model
from django.db import transaction

from google_2fa import app_settings

from .models import Google2FA, generate_reserve_key
from .utils import is_reserve_key_valid, make_reserve_key

User = get_user_model()


class Google2FARequest:
    API_KEY: str = app_settings.GOOGLE_2FA_API_KEY
    API_URL: str = app_settings.GOOGLE_2FA_URL
    ISSUER: str = app_settings.GOOGLE_2FA_ISSUER

    @property
    def headers(self) -> dict:
        return {
            "X-RapidAPI-Host": "google-authenticator.p.rapidapi.com",
            "X-RapidAPI-Key": self.API_KEY,
        }

    def qr_code_generate(self, account: str, issuer: str = None, secret: str = None) -> str:
        params = {
            "secret": secret,
            "issuer": issuer or self.ISSUER,
            "account": account,
        }
        url = app_settings.GOOGLE_2FA_ENDPOINTS['enroll']
        response = requests.get(url, headers=self.headers, params=params)
        return response.text.strip()

    def validate_code(self, code: str, secret: str) -> bool:
        url = app_settings.GOOGLE_2FA_ENDPOINTS['validate']
        params = {
            'code': code,
            'secret': secret,
        }
        response = requests.get(url, headers=self.headers, params=params)
        return True if response.text == 'True' else False

    def get_secret(self) -> str:
        url = app_settings.GOOGLE_2FA_ENDPOINTS['new_v2']
        response = requests.get(url, headers=self.headers)
        return response.text


class Google2FAHandler:
    @staticmethod
    def get_user(user_id: int):
        return User.objects.select_related('two_fa').get(id=user_id)

    @staticmethod
    def get_google_2fa(user) -> Optional[Google2FA]:
        try:
            return Google2FA.objects.get(user=user)
        except Google2FA.DoesNotExist:
            return None

    @staticmethod
    def generate_user_qr_code(user) -> dict:
        service = Google2FARequest()
        reserve_key: str = generate_reserve_key()
        secret: str = service.get_secret()
        qr_code: str = service.qr_code_generate(account=getattr(user, user.USERNAME_FIELD), secret=secret)
        data = {
            'qr_code': qr_code,
            'reserve_key': reserve_key,
            'secret': secret,
        }
        return data

    @staticmethod
    @transaction.atomic()
    def enable_user_2fa(user, secret: str, reserve_key: str):
        Google2FA.objects.create(
            user=user,
            secret=secret,
            reserve_key=make_reserve_key(reserve_key),
        )
        user.enable_2fa = True
        user.save(update_fields=['enable_2fa'])
        return user

    @staticmethod
    def validate_reserve_key(reserve_key: str, hashed_reserve_key: str) -> bool:
        return is_reserve_key_valid(reserve_key, hashed_reserve_key)

    @transaction.atomic()
    def deactivate_user_2fa(self, user):
        user.enable_2fa = False
        user.save(update_fields=['enable_2fa'])
        user.two_fa.delete()
        return user
