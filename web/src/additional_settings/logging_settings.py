L
OGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(levelname)s %(message)s"
        },
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        'console': {
            'class': 'logging.StreamHandler',
        },
        "null": {
            "class": "logging.NullHandler",
        },
    },

}
