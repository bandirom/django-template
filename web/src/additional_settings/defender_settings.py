from os import environ


DEFENDER_REDIS_URL = environ.get("REDIS_URL")
DEFENDER_USE_CELERY = False
