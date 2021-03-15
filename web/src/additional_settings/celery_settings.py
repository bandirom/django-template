from os import environ

RABBITMQ_URL = environ.get('RABBITMQ_URL')
REDIS_URL = environ.get('REDIS_URL')


CELERY_BROKER_URL = REDIS_URL + '/0'
CELERY_RESULT_BACKEND = REDIS_URL + '/0'
CELERY_TIMEZONE = "Europe/Kiev"

CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'


CELERY_BROKER_TRANSPORT_OPTIONS = {
    'max_retries': 4,
    'interval_start': 0,
    'interval_step': 0.5,
    'interval_max': 3,
}

CELERY_TASK_ROUTES = {
    '*': {'queue': 'celery'},
}
