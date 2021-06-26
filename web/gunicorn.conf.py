from multiprocessing import cpu_count
from os import environ


bind = ["0.0.0.0:8000", "unix:/gunicorn_socket/gunicorn.sock"]

workers = 3  # cpu_count() * 2 + 1

threads = 1

worker_class = 'uvicorn.workers.UvicornH11Worker'

loglevel = 'info'
accesslog = None  # environ.get('APP_HOME', '') + '/logs/gunicorn_access.log'

errorlog = '-'  # environ.get('APP_HOME', '') + '/logs/gunicorn_errors.log'

reload = False

max_requests = 1000
max_requests_jitter = 200

user = 1000
group = 1000
