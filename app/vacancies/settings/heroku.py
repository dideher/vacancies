import os
from vacancies.settings.common import *

DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']


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