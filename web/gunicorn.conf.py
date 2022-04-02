from multiprocessing import cpu_count
from os import environ

bind: list = ['unix:/gunicorn_socket/gunicorn.sock']

workers: int = int(environ.get('GUNICORN_WORKERS', cpu_count() * 2 + 1))

threads: int = int(environ.get('GUNICORN_THREADS', 1))

worker_class: str = 'uvicorn.workers.UvicornWorker'

loglevel: str = 'info'

accesslog = None  # environ.get('APP_HOME', '') + '/logs/gunicorn_access.log'
errorlog = '-'  # environ.get('APP_HOME', '') + '/logs/gunicorn_errors.log'

reload: bool = bool(environ.get('GUNICORN_RELOAD', 0))

# Reload gunicorn worker if request count > max_requests
max_requests: int = 1000
max_requests_jitter: int = 200

user: int = 1000
group: int = 1000

timeout: int = int(environ.get('GUNICORN_TIMEOUT', 30))

keepalive: int = int(environ.get('GUNICORN_KEEP_ALIVE', 2))
