from typing import TYPE_CHECKING

from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.settings import api_settings as jwt_settings
from rest_framework_simplejwt.tokens import RefreshToken

from api.v1.auth.types import AuthToken, RestAuthSettings, TokenResult
from main.models import UserT
from main.query_services import UserQueryService

if TYPE_CHECKING:
    from django.http import HttpResponse
    from rest_framework.request import Request


class LoginService:
    error_messages = {
        'not_active': 'Your account is not active. Please contact Your administrator',
        'wrong_credentials': 'Entered email or password is incorrect',
    }

    def __init__(
        self,
        request: "Request",
        settings: RestAuthSettings,
        user_query_service: UserQueryService | None = None,
    ):
        self._request = request
        self.user_query_service = user_query_service or UserQueryService()
        self._settings = settings

    def _authenticate(self, **kwargs: str) -> UserT | None:
        return authenticate(self._request, **kwargs)

    def validate_user_credentials(self, email: str, password: str) -> UserT:
        user = self._authenticate(email=email, password=password)
        if user is not None:
            return user

        user = self.user_query_service.get_by_email(email)
        if user is not None and not user.is_active:
            raise ValidationError({'email': self.error_messages['not_active']})

        raise ValidationError({'email': self.error_messages['wrong_credentials']})

    def get_tokens(self, user: UserT) -> AuthToken:
        tokens = self.__user_tokens(user)
        access_token_expiration, refresh_token_expiration = self.get_token_expirations()
        return TokenResult(
            access_token=tokens['access_token'],
            refresh_token=tokens['refresh_token'],
            access_token_expiration=access_token_expiration,
            refresh_token_expiration=refresh_token_expiration,
        )

    @staticmethod
    def __user_tokens(user: UserT) -> AuthToken:
        refresh = RefreshToken.for_user(user)
        return AuthToken(
            access_token=str(refresh.access_token),
            refresh_token=str(refresh),
        )

    @staticmethod
    def get_token_expirations():
        now = timezone.now()
        return (
            now + jwt_settings.ACCESS_TOKEN_LIFETIME,
            now + jwt_settings.REFRESH_TOKEN_LIFETIME,
        )

    def set_cookies(self, response: "HttpResponse", access_token: str, refresh_token: str):
        self._set_jwt_access_cookie(response, access_token)
        self._set_jwt_refresh_cookie(response, refresh_token)

    def __set_jwt_cookie(
        self,
        response: "HttpResponse",
        key: str,
        token_value: str,
        token_expiration: str,
    ) -> None:
        response.set_cookie(
            key=key,
            value=token_value,
            expires=token_expiration,
            secure=self._settings['JWT_AUTH_SECURE'],
            httponly=self._settings['JWT_AUTH_HTTPONLY'],
            samesite=self._settings['JWT_AUTH_SAMESITE'],
            domain=self._settings['JWT_COOKIE_DOMAIN'],
        )

    def _set_jwt_access_cookie(self, response: "HttpResponse", access_token: str):
        access_token_expiration = timezone.now() + jwt_settings.ACCESS_TOKEN_LIFETIME
        self.__set_jwt_cookie(response, self._settings['JWT_AUTH_COOKIE'], access_token, access_token_expiration)

    def _set_jwt_refresh_cookie(self, response: "HttpResponse", refresh_token: str):
        refresh_token_expiration = timezone.now() + jwt_settings.REFRESH_TOKEN_LIFETIME
        self.__set_jwt_cookie(
            response, self._settings['JWT_AUTH_REFRESH_COOKIE'], refresh_token, refresh_token_expiration
        )
