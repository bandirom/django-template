import logging
from functools import wraps
from timeit import default_timer
from typing import Any, Callable, TypeVar, Union

from django.core.cache import cache
from kombu.exceptions import OperationalError
from requests.exceptions import RequestException

from celery.exceptions import TimeoutError

logger = logging.getLogger(__name__)

RT = TypeVar('RT')


def cached_result(cache_key: str, timeout: int = 300, version: Union[int, str] = 1):
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


def execution_time(stdout: str = 'console'):
    """
    :param stdout: 'console' or 'tuple'
    """

    def decorator(func: Callable[..., RT]) -> Callable[..., RT]:
        @wraps(func)
        def delta_time(*args: Any, **kwargs: Any) -> RT:
            t1 = default_timer()
            data = func(*args, **kwargs)
            delta = default_timer() - t1
            if stdout == "console":
                logger.debug(f"Function: {func.__name__}, Run time: {delta}")
                logger.debug(f"Returned data: {data}, Type: {type(data)}")
                logger.debug("############ SEPARATING ############")
            elif stdout == "tuple":
                return data, delta
            return data

        return delta_time

    return decorator


def except_shell(errors=(Exception,), default_value: Any = None):
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
