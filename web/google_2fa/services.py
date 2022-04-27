
import requests
from google_2fa import app_settings

from .models import Google2FA


class Google2FAService:
    API_KEY: str = app_settings.GOOGLE_2FA_API_KEY
    API_URL: str = app_settings.GOOGLE_2FA_URL
    ISSUER: str = app_settings.GOOGLE_2FA_ISSUER

    @property
    def headers(self) -> dict:
        return {
            "X-RapidAPI-Host": "google-authenticator.p.rapidapi.com",
            "X-RapidAPI-Key": self.API_KEY,
        }

    def qr_code_generate(self, account: str, issuer: str = None) -> str:

        secret = self._get_secret()
        params = {
            "secret": secret,
            "issuer": issuer or self.ISSUER,
            "account": account,
        }
        url = app_settings.GOOGLE_2FA_ENDPOINTS['enroll']
        response = requests.get(url, headers=self.headers, params=params)
        return response.text

    def validate_code(self, code: str, secret: str) -> bool:
        url = app_settings.GOOGLE_2FA_ENDPOINTS['validate']
        params = {
            'code': code,
            'secret': secret,
        }
        response = requests.get(url, headers=self.headers, params=params)
        return True if response.text == 'True' else False

    def _get_secret(self) -> str:
        url = app_settings.GOOGLE_2FA_ENDPOINTS['new_v2']
        response = requests.get(url, headers=self.headers)
        return response.text
