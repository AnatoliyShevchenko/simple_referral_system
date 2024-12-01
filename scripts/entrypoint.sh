#!/bin/bash

echo "Waiting for PostgreSQL..."
/scripts/wait-for.sh simple-referral-system-postgres 5432 30

echo "Running database migrations..."
python manage.py migrate

echo "Collect static"
python manage.py collectstatic

echo "Starting the application..."
exec gunicorn --bind 0.0.0.0:8000 settings.wsgi
