#!/usr/bin/env bash
set -e

# Esperar DB (opcional, para Postgres). Puedes instalar 'wait-for-it' o usar sleep corto.
# sleep 5

echo "Aplicando migraciones..."
python manage.py migrate --noinput

echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

# Lanzar Gunicorn
exec gunicorn nequi.wsgi:application --bind 0.0.0.0:8000 --workers 3
