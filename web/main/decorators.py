import logging
from functools import wraps
from smtplib import SMTPRecipientsRefused
from timeit import default_timer
from typing import Union

from django.core.cache import cache
from kombu.exceptions import OperationalError
from requests.exceptions import RequestException

from celery.exceptions import TimeoutError

logger = logging.getLogger(__name__)


def cached_result(cache_key: str, timeout: int = 300, version: Union[int, str] = 1):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
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

    def decorator(func):
        @wraps(func)
        def delta_time(*args, **kwargs):
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


def except_shell(errors=(Exception,), default_value=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except errors as e:
                logging.error(e)
                return default_value

        return wrapper

    return decorator


request_shell = except_shell((RequestException,))
celery_shell = except_shell((OperationalError, TimeoutError))
smtp_shell = except_shell((SMTPRecipientsRefused,), default_value=False)
