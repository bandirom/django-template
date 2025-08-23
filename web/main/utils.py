from typing import Any


def parse_str_with_space(var: str) -> str:
    """Return string without multiple whitespaces.

    Example:
        var = 'My name  is   John    '
        return 'My name is John'

    """
    str_list = list(filter(None, var.split(' ')))
    return ' '.join(x for x in str_list)


def find_dict_in_list(target: list[dict], dict_key: str | int, lookup_value: Any) -> dict:
    """Find a dict in a list of dict by dict key."""
    return next(iter(x for x in target if x.get(dict_key) == lookup_value), {})
