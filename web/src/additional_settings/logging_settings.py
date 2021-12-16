from os import environ

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {'level': 'INFO', 'handlers': ['default']},
    'formatters': {
        'simple': {'format': '%(levelname)s %(message)s'},
        'verbose': {'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'},
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[{server_time}] {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'null': {
            'class': 'logging.NullHandler',
        },
        'default': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
    },
    'loggers': {
        'django': {'level': 'INFO', 'propagate': True},
        'django.request': {
            'handlers': ['django.server'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
