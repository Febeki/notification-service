#!/bin/sh

python manage.py wait_for_db

python manage.py makemigrations
python manage.py migrate

python manage.py create_superuser

python manage.py collectstatic --noinput


exec "$@"