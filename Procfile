release: cd app && python manage.py migrate --noinput
web: gunicorn --pythonpath app vacancies.wsgi --log-file=-
