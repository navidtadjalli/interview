"""
Django settings for achare_interview project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path
from achare_interview.constants import EnvVarKeys
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-o&4#b-h@n+19y22g@0lh5!x(fhqt)u^e=@f05u+%$#251j1v$4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'customer.apps.CustomerConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'achare_interview.utils.middlewares.AttemptMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'achare_interview.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'achare_interview.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = "customer.Customer"

SENSITIVE_ENDPOINTS = [
    "/register",
    "/login"
]

# Redis data configurations
REDIS_HOST = os.environ.get(EnvVarKeys.RedisHost, "localhost")
REDIS_PORT = os.environ.get(EnvVarKeys.RedisPort, "6379")
REDIS_VALIDATION_CODE_DB = os.environ.get(EnvVarKeys.RedisValidationCodeDB, "1")
REDIS_REGISTRATION_TOKEN_DB = os.environ.get(EnvVarKeys.RedisRegistrationTokenDB, "2")
REDIS_ATTEMPTS_DB = os.environ.get(EnvVarKeys.RedisAttemptsDB, "3")
REDIS_BLOCKED_DB = os.environ.get(EnvVarKeys.BlockedDB, "4")

GENERATED_CODE_TIME_TO_LIVE = int(os.environ.get(EnvVarKeys.GeneratedCodeTimeToLive, 120))
REGISTRATION_TOKEN_TIME_TO_LIVE = int(os.environ.get(EnvVarKeys.RegistrationTokenTimeToLive, 600))
ATTEMPTS_TIME_TO_LIVE = int(os.environ.get(EnvVarKeys.AttemptsTimeToLive, 3600))
BLOCKED_KEY_TIME_TO_LIVE = int(os.environ.get(EnvVarKeys.BlockedKeyTimeToLive, 3600))

MAXIMUM_CODE_REQUEST_COUNT = int(os.environ.get(EnvVarKeys.MaximumCodeRequestCount, 3))

GENERATE_FAKE_CODE = True \
    if str(os.environ.get(EnvVarKeys.GenerateFakeCode, "0")).lower() in ('1', 'yes', 'y', 'true') \
    else False
