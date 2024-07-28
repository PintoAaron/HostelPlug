#!/bin/sh

python manage.py migrate
python manage.py create_admin
python manage.py collectstatic --no-input
gunicorn HostelPlug.wsgi:application --bind 0.0.0.0:8000
celery -A HostelPlug worker -l info
celery -A HostelPlug beat -l info