#!/bin/sh
python3 manage.py makemigrations
python3 manage.py migrate
export DJANGO_SUPERUSER_USERNAME=admin
export DJANGO_SUPERUSER_EMAIL=admin@example.com
export DJANGO_SUPERUSER_PASSWORD=root
python3 manage.py createsuperuser --noinput
export DJANGO_SETTINGS_MODULE=backend.settings_docker
python3 initial_script.py
daphne backend.asgi:application -b 0.0.0.0 -p 8000