from typing import Any

from django.utils.translation import get_language_from_request


def parse_str_with_space(var: str) -> str:
    """return string without multiply whitespaces
    Example: var = 'My name  is   John    '
    Return var = 'My name is John'
    """
    str_list = list(filter(None, var.split(' ')))
    return ' '.join(x for x in str_list)


def find_dict_in_list(target: list[dict], dict_key: str | int, lookup_value: Any) -> dict:
    """Find a dict in a list of dict by dict key"""
    return next(iter(x for x in target if x.get(dict_key) == lookup_value), {})


def get_supported_user_language(request) -> str:
    return get_language_from_request(request)
