import os
from vacancies.settings.common import *

DEBUG = True

SECRET_KEY = os.environ['SECRET_KEY']

# Email settings
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey' # this is exactly the value 'apikey'
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
EMAIL_PORT = 587
EMAIL_USE_TLS = True


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}



# Configure Django App for Heroku.
try:
    import django_heroku
    django_heroku.settings(locals())
except ImportError:
    # probably not running on Heroku
    pass