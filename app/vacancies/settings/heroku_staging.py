import os
from vacancies.settings.common import *

DEBUG = True

SECRET_KEY = os.environ['SECRET_KEY']

# Email settings
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
DEFAULT_FROM_EMAIL = 'no-reply-staging@dideira.gr'
EMAIL_SUBJECT_PREFIX = '[kena_staging] '

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