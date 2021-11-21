from os import environ


DEFENDER_REDIS_URL = environ.get("REDIS_URL", 'redis://redis:6379') + '/1'
DEFENDER_USE_CELERY = False
