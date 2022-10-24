import os
from vacancies.settings.common import *

DEBUG = True

SECRET_KEY = os.environ['SECRET_KEY']

# Email settings
DEFAULT_FROM_EMAIL = 'no-reply-staging@dideira.gr'
EMAIL_SUBJECT_PREFIX = '[kena_staging] '


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

# Sentry Settings
try:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=os.getenv('SENTRY_DSN'),
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        environment=os.getenv('SENTRY_ENVIRONMENT'),

        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True
    )
except ImportError:
    # probably dependecies not installed
    pass