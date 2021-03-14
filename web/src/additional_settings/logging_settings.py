from os import environ


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {"level": "INFO", "handlers": ["default"]},
    "formatters": {
        "simple": {
            "format": "%(levelname)s %(message)s"
        },
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"
        },
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] {message}",
            "style": "{",
        },
        "json": {
            "()": "main.logging.JsonFormatter",
            "datefmt": "%Y-%m-%dT%H:%M:%SZ",
            "format": (
                "%(asctime)s %(levelname)s %(lineno)s %(message)s %(name)s %(pathname)s %(process)d %(threadName)s"
            ),
        },
    },
    "handlers": {
        'console': {
            'class': 'logging.StreamHandler',
        },
        "null": {
            "class": "logging.NullHandler",
        },
        "default": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose" if environ.get('DEBUG') else "json",
        },
        "django.server": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "django.server" if environ.get('DEBUG') else "json",
        },
    },
    "loggers": {
        "django": {
            "level": "INFO",
            "propagate": True
        },
        "django.server": {
            "handlers": ["django.server"],
            "level": "INFO",
            "propagate": False,
        },
    },

}
