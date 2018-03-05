"""
Django settings for crtr project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from envparse import env
env.read_envfile('.env')

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Quick-start development settings - unsuitable for PRODUCTION
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in PRODUCTION secret!
SECRET_KEY = 'c5o%6-up-b%f7@vv-+vt^fv1pg61*t^3b$2j0#73g5xn-p&5)q'

# SECURITY WARNING: don't run with debug turned on in PRODUCTION!
DEBUG = env('DEBUG', True, cast=bool)
PRODUCTION = env('PRODUCTION', not DEBUG, cast=bool)
USE_HEROKU = env('USE_HEROKU', False, cast=bool)

ALLOWED_HOSTS = ['spectacles.peterdowns.com', 'localhost', 'peterdowns.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Libraries
    'django_elasticsearch_dsl',
    # Our code
    #'specutron', # Analysis
    'app',
    'datastore',
]

AUTH_USER_MODEL = 'app.User'
LOGIN_URL = 'auth-login'
LOGIN_REDIRECT_URL = 'app-documents'
LOGOUT_REDIRECT_URL = 'auth-login'
APPEND_SLASH = False

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'local': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'spectacles',
        'USER': 'spectacles',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',
    },
    'heroku' : {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('HEROKU_PG_NAME', None),
        'PORT': env('HEROKU_PG_PORT', None),
        'HOST': env('HEROKU_PG_HOST', None),
        'USER': env('HEROKU_PG_USER', None),
        'PASSWORD': env('HEROKU_PG_PASSWORD', None),
    },
    'sqlite': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
}
ELASTICSEARCH_DSL = {
    'local': {
        'hosts': 'localhost:9200',
        'timeout': 30,
    },
    'heroku': {
        'hosts': 'https://{user}:{password}@{host}'.format(
            user=env('HEROKU_ES_USER', ''),
            password=env('HEROKU_ES_PASSWORD', ''),
            host=env('HEROKU_ES_HOST', ''),
        ),
        'port': env('HEROKU_ES_PORT', None),
        'timeout': 30,
        'use_ssl': True,
    },
}

def set_default(d):
    d['default'] = d['heroku' if USE_HEROKU else 'local']

set_default(DATABASES)
set_default(ELASTICSEARCH_DSL)
print(ELASTICSEARCH_DSL['default']['hosts'])

# Elasticsearch Indexing
ES_IGNORE_SIGNALS = env('ES_IGNORE_SIGNALS', False)
ES_AUTO_REFRESH = env('ES_AUTO_REFRESH', True)



# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = False

USE_L10N = False

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static'),
    ]
