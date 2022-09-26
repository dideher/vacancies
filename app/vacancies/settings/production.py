import os
from vacancies.settings.common import *

DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']

# Email settings
DEFAULT_FROM_EMAIL = 'no-reply@dideira.gr'
EMAIL_SUBJECT_PREFIX = '[kena] '

# SECURITY WARNING: update this when you have the production host
ALLOWED_HOSTS = ['0.0.0.0', 'localhost']


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'vacancies_db',
        'USER': 'user',
        'PASSWORD': 'password',
        'HOST': 'db',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': 'SET default_storage_engine=INNODB',
        }
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_ROOT = "/app/static_files"