#!/bin/bash

python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput
python manage.py runserver 0.0.0.0:8000
python manage.py create_superuser
