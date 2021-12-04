#!/bin/sh

python manage.py wait_for_db

python manage.py check --deploy

python manage.py migrate
python manage.py collectstatic --no-input

gunicorn src.asgi:application
