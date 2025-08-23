#!/bin/sh

python manage.py wait_for_db

python manage.py check --deploy

python manage.py migrate

nginx -g 'daemon on;'

gunicorn -c src/gunicorn.conf.py src.asgi:application
