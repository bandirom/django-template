from typing import TypedDict


class AuthToken(TypedDict):
    access_token: str
    refresh_token: str


class TokenResult(AuthToken):
    access_token_expiration: str
    refresh_token_expiration: str


class RestAuthSettings(TypedDict):
    JWT_AUTH_REFRESH_COOKIE: str
    JWT_AUTH_COOKIE: str
    JWT_AUTH_HTTPONLY: bool
    JWT_AUTH_SAMESITE: str
    JWT_AUTH_SECURE: str
    JWT_COOKIE_DOMAIN: str
