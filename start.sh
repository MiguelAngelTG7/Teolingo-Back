#!/bin/bash
python manage.py collectstatic --noinput
python manage.py migrate
gunicorn biblielingo_back.wsgi:application --config gunicorn.conf.py