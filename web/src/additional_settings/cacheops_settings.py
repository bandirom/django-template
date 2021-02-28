from os import environ

CACHEOPS_REDIS = environ.get('REDIS_URL') + "/2"

CACHEOPS_DEFAULTS = {
    'timeout': 60 * 60
}

CACHEOPS = {
    'main.user': {'ops': 'get', 'timeout': 60 * 15},
}
