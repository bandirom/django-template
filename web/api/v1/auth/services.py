from datetime import UTC, datetime
from typing import TYPE_CHECKING

from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from api.v1.auth.types import RestAuthSettings, TokenResult
from main.query_services import UserQueryService

if TYPE_CHECKING:
    from django.http import HttpResponse
    from rest_framework.request import Request

    from main.models import UserT


class LoginService:
    _error_messages = {
        'not_active': 'Your account is not active. Please contact Your administrator',
        'wrong_credentials': 'Entered email or password is incorrect',
    }

    def __init__(
        self,
        request: "Request",
        settings: "RestAuthSettings",
        user_query_service: "UserQueryService | None" = None,
    ):
        self._request = request
        self.user_query_service = user_query_service or UserQueryService()
        self._settings = settings

    def _authenticate(self, **kwargs: str) -> "UserT | None":
        return authenticate(self._request, **kwargs)

    def validate_user_credentials(self, email: str, password: str) -> "UserT":
        user = self._authenticate(email=email, password=password)
        if user is not None:
            return user

        user = self.user_query_service.get_by_email(email)
        if user is not None and not user.is_active:
            raise ValidationError({'email': self._error_messages['not_active']})

        raise ValidationError({'email': self._error_messages['wrong_credentials']})

    def get_tokens(self, user: "UserT") -> TokenResult:
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        return TokenResult(
            access_token=str(access),
            refresh_token=str(refresh),
            access_token_expiration=datetime.fromtimestamp(access['exp'], tz=UTC),
            refresh_token_expiration=datetime.fromtimestamp(refresh['exp'], tz=UTC),
        )

    def set_cookies(self, response: "HttpResponse", tokens: TokenResult) -> None:
        self._set_jwt_access_cookie(response, tokens['access_token'], tokens['access_token_expiration'])
        self._set_jwt_refresh_cookie(response, tokens['refresh_token'], tokens['refresh_token_expiration'])

    def __set_jwt_cookie(
        self,
        response: "HttpResponse",
        key: str,
        token_value: str,
        token_expiration: datetime,
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

    def _set_jwt_access_cookie(self, response: "HttpResponse", key: str, expiration: datetime) -> None:
        self.__set_jwt_cookie(
            response,
            self._settings['JWT_AUTH_COOKIE'],
            key,
            expiration,
        )

    def _set_jwt_refresh_cookie(self, response: "HttpResponse", key: str, expiration: datetime) -> None:
        self.__set_jwt_cookie(
            response,
            self._settings['JWT_AUTH_REFRESH_COOKIE'],
            key,
            expiration,
        )
