import logging
from django.core.cache import cache
from requests.exceptions import RequestException
from kombu.exceptions import OperationalError
from celery.exceptions import TimeoutError
from timeit import default_timer
from smtplib import SMTPRecipientsRefused

logger = logging.getLogger(__name__)


def cached_function_result(timeout: int = 300, version: int = 1, prefix: str = ''):
    def decorator(function):
        def wrapper(*args, **kwargs):
            key = prefix + '_' + function.__name__ if prefix else function.__name__
            if key in cache:
                return cache.get(key)
            result = function(*args, **kwargs)
            cache.set(key, result, timeout=timeout, version=version)
            return result
        return wrapper
    return decorator


def execution_time(stdout: str = 'console'):
    """
    :param stdout: 'console' or 'tuple'
    """
    def decorator(func) -> object:
        def delta_time(*args, **kwargs):
            t1 = default_timer()
            data = func(*args, **kwargs)
            delta = default_timer() - t1
            if stdout == 'console':
                logger.info(f'Function: {func.__name__}, Run time: {delta}')
                logger.info(f'Returned data: {data}, Type: {type(data)}')
                logger.info('############ SEPARATING ############')
            elif stdout == 'tuple':
                return data, delta
            return data
        return delta_time
    return decorator


def except_shell(errors=(Exception,), default_value=None):
    def decorator(func):
        def new_func(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except errors as e:
                logging.error(e)
                return default_value
        return new_func
    return decorator


request_shell = except_shell((RequestException,))
celery_shell = except_shell((OperationalError, TimeoutError))
smtp_shell = except_shell((SMTPRecipientsRefused,), default_value=False)
