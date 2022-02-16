#!/bin/bash

python3 manage.py migrate

python3 manage.py collectstatic --no-input

exec gunicorn config.wsgi:application -b 0.0.0.0:8000 --reload
