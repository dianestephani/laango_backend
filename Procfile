release: python3 manage.py migrate --noinput
web: gunicorn laango.wsgi:application --bind 0.0.0.0:$PORT
