from django.core import signing
from . import app_settings


def make_reserve_key(reserve_key: str) -> str:
    return signing.dumps(reserve_key, salt=app_settings.RESERVE_KEY_SALT)


def is_reserve_key_valid(reserve_key: str) -> bool:
    try:
        signing.loads(reserve_key, salt=app_settings.RESERVE_KEY_SALT)
        return True
    except:
        return False
