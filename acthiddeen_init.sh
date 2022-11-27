#!/bin/sh

echo "[ACTS] PREPARE DATABASE..."
echo "[ACTS] Для alpine linux используется #!/bin/sh для deb - #!/bin/bash"

# cd ./app/acts

echo "[ACTS] Collect static files..."
python manage.py collectstatic --noinput

# echo "Получение дампа данных только при первом запуске контейнера"
# python manage.py loaddata datadump.json

# echo "Apply database migrations... только при первом запуске контейнера"
# python manage.py migrate

echo "[ACTS] Starting server..."
# echo "[ACTS] Django development server..."
# python manage.py runserver 0.0.0.0:8000

echo "[ACTS] Gunicorn server"
gunicorn -b 0.0.0.0:8000 acts.wsgi:application

