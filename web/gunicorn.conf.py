from multiprocessing import cpu_count


bind = "0.0.0.0:8000"
# bind = "unix:/gunicorn/gunicorn.sock"
# workers = cpu_count() * 2 + 1

workers = 3
worker_class = 'uvicorn.workers.UvicornH11Worker'
loglevel = 'info'
reload = True
