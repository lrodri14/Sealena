"""
Django settings for Sealena project.

Generated by 'django-admin startproject' using Django 3.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
DOT_ENV = os.path.join(BASE_DIR, '.env')

load_dotenv(DOT_ENV)

# PRODUCTION SETTINGS
SECRET_KEY = os.environ.get('SEALENA_SECRET_KEY')
DEBUG = False

if not DEBUG:
    ALLOWED_HOSTS = os.environ.get('SEALENA_ALLOWED_HOSTS').split(',')
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
else:
    ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    'main',
    'home',
    'accounts',
    'patients',
    'appointments',
    'records',
    'stats',
    'settings',
    'providers',
]

# CUSTOM USER MODEL REFERENCE
AUTH_USER_MODEL = 'accounts.CustomUser'

# PASSWORD HASHERS
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

# MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'accounts.middleware.LoginRequiredMiddleware',
    'accounts.middleware.TimezoneMiddleware',
]

# URL CONF
ROOT_URLCONF = 'Sealena.urls'

# TEMPLATES
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

# X-FRAME
X_FRAME_OPTIONS = 'SAMEORIGIN'

# EMAIL SETTINGS
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.zoho.com'
EMAIL_PORT = '587'
EMAIL_HOST_USER = os.environ.get('SEALENA_EMAIL')
EMAIL_HOST_PASSWORD = os.environ.get('SEALENA_EMAIL_PASSWORD')
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = os.environ.get('SEALENA_EMAIL')

# WSGI - ASGI
WSGI_APPLICATION = 'Sealena.wsgi.application'
ASGI_APPLICATION = 'Sealena.asgi.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

if not DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ.get('SEALENA_DB_NAME'),
            'USER': os.environ.get('SEALENA_DB_USER'),
            'PASSWORD': os.environ.get('SEALENA_DB_PASSWORD'),
            'HOST': os.environ.get('SEALENA_DB_HOST'),
            'PORT': os.environ.get('SEALENA_DB_PORT'),
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
            }
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DATETIME_FORMAT = '%Y-%m-%dT%H:%M'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_URL = '/staticfiles/'
STATICFILES_DIRS = [STATIC_DIR]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media Files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# NUMVERIFY
NUMVERIFY_ENDPOINT = os.environ.get('NUMVERIFY_ENDPOINT')
NUMVERIFY_API_KEY = os.environ.get('NUMVERIFY_API_KEY')

# RAPID_API
X_RAPID_API_QUOTES_ENDPOINT = os.environ.get('X_RAPID_API_QUOTES_ENDPOINT')
X_RAPID_API_KEY_QUOTES = os.environ.get('X_RAPID_API_KEY_QUOTES')
X_RAPID_API_KEY_HOST_QUOTES = os.environ.get('X_RAPID_API_KEY_HOST_QUOTES')

# TWILIO
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')

# PAYPAL
PAYPAL_AUTH_TOKEN_REQ_ENDPOINT = os.environ.get('PAYPAL_AUTH_TOKEN_REQ_ENDPOINT')
PAYPAL_CREATE_PRODUCT_ENDPOINT = os.environ.get('PAYPAL_CREATE_PRODUCT_ENDPOINT')
PAYPAL_CREATE_PLAN_ENDPOINT = os.environ.get('PAYPAL_CREATE_PLAN_ENDPOINT')
PAYPAL_CANCEL_SUBSCRIPTION_ENDPOINT = os.environ.get('PAYPAL_CANCEL_SUBSCRIPTION_ENDPOINT')
PAYPAL_CLIENT_ID = os.environ.get('PAYPAL_CLIENT_ID')
PAYPAL_SECRET_KEY = os.environ.get('PAYPAL_SECRET_KEY')
PAYPAL_ACCESS_TOKEN = os.environ.get('PAYPAL_ACCESS_TOKEN')

# LOGIN/LOGOUT REDIRECTION
LOGIN_URL = '/lobby/'
LOGIN_REDIRECT_URL = '/home/'
LOGOUT_REDIRECT_URL = '/lobby/'
