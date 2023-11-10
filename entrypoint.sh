#!/bin/sh

python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Copia os arquivos estáticos para o diretório do Nginx
cp -r /usr/src/app/staticfiles/* /staticfiles/

# Inicia o Gunicorn como servidor WSGI
gunicorn opportunity.wsgi:application --bind 0.0.0.0:8000
