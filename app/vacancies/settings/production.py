import os
from vacancies.settings.common import *

DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']

# Email settings
DEFAULT_FROM_EMAIL = 'no-reply@dideira.gr'
EMAIL_SUBJECT_PREFIX = '[kena] '

ALLOWED_HOSTS = ['localhost', '0.0.0.0', '127.0.0.1', 'kena.dideira.gr']


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASS'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT', 3306),
        'OPTIONS': {
            'init_command': "SET default_storage_engine=INNODB; SET sql_mode='STRICT_TRANS_TABLES'",
            'isolation_level': 'read committed',
        }
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATIC_ROOT = '/app/static_files'
MEDIA_ROOT = '/app/media_files'