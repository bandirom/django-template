#!/bin/sh

echo "Setting test env"

python manage.py wait_for_db

python manage.py test main --no-input
exec "$@"
