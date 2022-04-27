from django.core import signing
from . import app_settings


def make_reserve_key(reserve_key: str) -> str:
    return signing.dumps(reserve_key, salt=app_settings.TWO_FA_RESERVE_KEY_SALT)


def is_reserve_key_valid(reserve_key: str, hashed_reserve_key: str) -> bool:
    try:
        decoded = signing.loads(hashed_reserve_key, salt=app_settings.TWO_FA_RESERVE_KEY_SALT)
        return reserve_key == decoded
    except (signing.BadSignature, signing.SignatureExpired):
        return False
