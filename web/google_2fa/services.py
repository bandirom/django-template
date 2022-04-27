from typing import Optional
from django.contrib.auth import get_user_model

import requests
from google_2fa import app_settings

from .models import Google2FA, generate_reserve_key

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
        if not secret:
            secret = self.get_secret()
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
    def get_google_2fa(user) -> Optional[Google2FA]:
        try:
            return Google2FA.objects.get(user=user)
        except User.DoesNotExist:
            return None

    def generate_user_qr_code(self, user):
        service = Google2FARequest()
        google_2fa = self.get_google_2fa(user)
        if not google_2fa:
            reserve_key = generate_reserve_key()
            Google2FA.objects.create(
                user=user,
                secret=service.get_secret(),
            )

