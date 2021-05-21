from os import environ


DEFENDER_REDIS_URL = environ.get("REDIS_URL") + '/1'
DEFENDER_USE_CELERY = False
