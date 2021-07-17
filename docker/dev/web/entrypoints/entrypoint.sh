#!/bin/sh

python manage.py wait_for_db

python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000

# If you use Uvicorn please also run collectstatic command
#python manage.py collectstatic --no-input
#uvicorn src.asgi:application --host 0.0.0.0 --port 8000 --log-level debug --reload
