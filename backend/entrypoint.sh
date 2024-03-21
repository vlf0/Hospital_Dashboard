#!/bin/sh
python3 manage.py collectstatic --noinput
celery -A backend worker -l INFO -P threads
celery -A backend beat -l INFO
daphne backend.asgi:application -p 8000
