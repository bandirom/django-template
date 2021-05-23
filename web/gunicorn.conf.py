from multiprocessing import cpu_count


# workers = cpu_count() * 2 + 1
bind = ["0.0.0.0:8000", "unix:/gunicorn_socket/gunicorn.sock"]
workers = 3
worker_class = 'uvicorn.workers.UvicornH11Worker'
loglevel = 'info'
reload = True
