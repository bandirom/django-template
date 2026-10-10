from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.utils import timezone
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from api.v1.auth.types import AuthToken
from main.models import UserT
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.http import HttpResponse


User = get_user_model()

class LoginService:
    response_serializer = LoginResponseSerializer

    error_messages = {
        'not_active': 'Your account is not active. Please contact Your administrator',
        'wrong_credentials': 'Entered email or password is incorrect',
    }

    def __init__(self, request):
        self.request = request
        self.settings: dict = settings.REST_AUTH

    def _authenticate(self, **kwargs: str):
        return authenticate(self.request, **kwargs)

    def validate_user_credentials(self, email: str, password: str) -> UserT:
        user = self._authenticate(email=email, password=password)
        if not user:
            user = self.get_user(email)
            if not user:
                msg = {'email': self.error_messages['wrong_credentials']}
                raise ValidationError(msg)
            if not user.is_active:
                msg = {'email': self.error_messages['not_active']}
                raise ValidationError(msg)
            msg = {'email': self.error_messages['wrong_credentials']}
            raise ValidationError(msg)
        return user

    def __user_tokens(self, user: UserT) -> AuthToken:
        refresh: RefreshToken = RefreshToken().for_user(user)
        return AuthToken(
            access_token=str(refresh.access_token),
            refresh_token=str(refresh),
        )

    def get_response(self, user: UserT):
        access_token, refresh_token = self.__user_tokens(user)
        access_token_expiration = timezone.now() + jwt_settings.ACCESS_TOKEN_LIFETIME
        refresh_token_expiration = timezone.now() + jwt_settings.REFRESH_TOKEN_LIFETIME
        return_expiration_times = getattr(settings, 'JWT_AUTH_RETURN_EXPIRATION', False)
        data = {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user,
        }
        if return_expiration_times:
            data['access_token_expiration'] = access_token_expiration
            data['refresh_token_expiration'] = refresh_token_expiration
        serializer = self.response_serializer(data)

        response = Response(serializer.data, status=HTTP_200_OK)
        self._set_jwt_cookies(response, access_token, refresh_token)
        return response

    def _set_jwt_cookies(self, response, access_token, refresh_token):
        self._set_jwt_access_cookie(response, access_token)
        self._set_jwt_refresh_cookie(response, refresh_token)

    def __set_jwt_cookie(self, response, key: str, token_value: str, token_expiration) -> None:
        response.set_cookie(
            key=key,
            value=token_value,
            expires=token_expiration,
            secure=self.settings['JWT_AUTH_SECURE'],
            httponly=self.settings['JWT_AUTH_HTTPONLY'],
            samesite=self.settings['JWT_AUTH_SAMESITE'],
            domain=self.settings['JWT_COOKIE_DOMAIN'],
        )

    def _set_jwt_access_cookie(self, response: "HttpResponse", access_token: str):
        access_token_expiration = timezone.now() + jwt_settings.ACCESS_TOKEN_LIFETIME
        self.__set_jwt_cookie(response, self.settings['JWT_AUTH_COOKIE'], access_token, access_token_expiration)

    def _set_jwt_refresh_cookie(self, response: "HttpResponse", refresh_token: str):
        refresh_token_expiration = timezone.now() + jwt_settings.REFRESH_TOKEN_LIFETIME
        self.__set_jwt_cookie(
            response, self.settings['JWT_AUTH_REFRESH_COOKIE'], refresh_token, refresh_token_expiration
        )
