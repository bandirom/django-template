import logging
from collections.abc import Callable, Iterable
from functools import wraps
from typing import Any, TypeVar

from django.core.cache import cache
from kombu.exceptions import OperationalError
from requests.exceptions import RequestException

from celery.exceptions import TimeoutError

logger = logging.getLogger(__name__)

RT = TypeVar('RT')


def cached_result(
    cache_key: str, timeout: int = 300, version: int | str = 1
) -> Callable[[Callable[..., RT]], Callable[..., RT]]:
    """Cache the result of a function using Django's cache system.

    This decorator stores the function's return value in the cache
    for the specified duration. If the value is already cached, it
    returns the cached result instead of calling the function again.

    :param cache_key: The key to store and retrieve the cached result.
    :param timeout: Cache timeout in seconds (default: 300).
    :param version: Cache version identifier (default: 1).
    :return: A decorator that caches the result of the wrapped function.
    """

    def decorator(function: Callable[..., RT]) -> Callable[..., RT]:
        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> RT:
            key = cache.make_key(cache_key, version)
            if key in cache:
                return cache.get(key)
            result = function(*args, **kwargs)
            cache.set(key, result, timeout=timeout)
            return result

        return wrapper

    return decorator


def except_shell(
    errors: Iterable = (Exception,), default_value: Any = None
) -> Callable[[Callable[..., RT]], Callable[..., RT]]:
    """Catch specific exceptions and return a default value.

    This decorator wraps a function and catches the given exceptions.
    If an exception occurs, it logs the error and returns the specified default value.

    :param errors: Iterable of exception classes to catch (default: (Exception,)).
    :param default_value: Value to return if an exception is caught (default: None).
    :return: A decorated function that handles specified exceptions.
    """

    def decorator(func: Callable[..., RT]) -> Callable[..., RT]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> RT:
            try:
                return func(*args, **kwargs)
            except errors as e:
                logging.error(e)
                return default_value

        return wrapper

    return decorator


request_shell = except_shell((RequestException,))
celery_shell = except_shell((OperationalError, TimeoutError))
