release: python manage.py migrate
web: gunicorn bundl_finance.wsgi --log-file -
worker: celery -A bundl_finance worker -l INFO
