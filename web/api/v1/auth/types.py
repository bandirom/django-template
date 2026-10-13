from datetime import datetime
from typing import TypedDict


class AuthToken(TypedDict):
    access_token: str
    refresh_token: str


class TokenExpiration(TypedDict):
    access_token_expiration: datetime
    refresh_token_expiration: datetime


class TokenResult(AuthToken, TokenExpiration):
    pass


class RestAuthSettings(TypedDict):
    JWT_AUTH_REFRESH_COOKIE: str
    JWT_AUTH_COOKIE: str
    JWT_AUTH_HTTPONLY: bool
    JWT_AUTH_SAMESITE: str
    JWT_AUTH_SECURE: bool
    JWT_COOKIE_DOMAIN: str | None
