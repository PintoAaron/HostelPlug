#!/bin/sh

# Wait for the database to be ready
while ! nc -z db 5432; do
  echo "Waiting for PostgreSQL..."
  sleep 1
done

echo "PostgreSQL is ready."

# Run migrations and then start the server
python manage.py migrate
python manage.py create_admin
python manage.py collectstatic --no-input
gunicorn HostelPlug.wsgi:application --bind 0.0.0.0:8000