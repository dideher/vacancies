from vacancies.settings.common import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ze7xy@oo3m#6g-%gs@)@49jvvrxw^&bgagkqby)sc1!kk95j7^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'db_vacancies'),
        'USER': os.getenv('DB_USER', 'vacancies_user'),
        'PASSWORD': os.getenv('DB_PASS', 'vacancies_pass'),
        'HOST': os.getenv('DB_HOST', 'db'),
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

