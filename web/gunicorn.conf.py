from multiprocessing import cpu_count
from os import environ


bind = ["0.0.0.0:8000", "unix:/gunicorn_socket/gunicorn.sock"]

workers: int = environ.get('GUNICORN_WORKERS', cpu_count() * 2 + 1)

threads: int = environ.get('GUNICORN_THREADS', 1)

worker_class = 'uvicorn.workers.UvicornWorker'

loglevel = 'info'

accesslog = None  # environ.get('APP_HOME', '') + '/logs/gunicorn_access.log'
errorlog = '-'  # environ.get('APP_HOME', '') + '/logs/gunicorn_errors.log'

reload = bool(environ.get('GUNICORN_RELOAD', 0))

# Reload gunicorn worker if request count > max_requests
max_requests = 1000
max_requests_jitter = 200

user = 1000
group = 1000

timeout: int = environ.get('GUNICORN_TIMEOUT', 30)

keepalive: int = environ.get('GUNICORN_KEEP_ALIVE', 2)
