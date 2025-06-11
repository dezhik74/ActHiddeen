#!/bin/sh
set -e

cd /code

echo "[ACTS] Collect static files..."
python manage.py collectstatic --noinput

# Пока не используем
#echo "[ACTS] Check migrations..."
#./check_migrations.sh

# echo "[ACTS] Starting dev server..."
# echo "Django development server..."
# python manage.py runserver 0.0.0.0:8000

echo "[ACTS] Gunicorn server"
gunicorn --config gunicorn.conf.py config.wsgi

