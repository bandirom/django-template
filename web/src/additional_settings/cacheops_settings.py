from os import environ

REDIS_URL = environ.get('REDIS_URL')
REDIS_SOCKET = environ.get('REDIS_SOCKET')

CACHEOPS_REDIS = {
    'host': 'redis',
    'port': 6379,
    'db': 1,
    'socket_timeout': 3,
    'unix_socket_path': REDIS_SOCKET
}

CACHEOPS_DEFAULTS = {
    'timeout': 60 * 60
}

CACHEOPS = {
    'main.user': {'ops': 'get', 'timeout': 60 * 15},
}
