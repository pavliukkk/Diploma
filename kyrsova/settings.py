"""
Django settings for kyrsova project.

Generated by 'django-admin startproject' using Django 4.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from django.utils.translation import gettext_lazy as _
import os
import dj_database_url
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-o%ql_ulfpek&i%#&)t^a+y9h@y#o^)#c$so5!x57ggp4g7=q_&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

gettext = lambda s: s
LANGUAGES = (
('uk', gettext('Ukrainian')),
('en','English')
)

DATABASE_URL = "mysql://root:kKMtYqiuPzmypLCpWKhXdciMgeDUaRhU@viaduct.proxy.rlwy.net:51971/railway"

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'kyrsova',
    'whitenoise.runserver_nostatic',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

ROOT_URLCONF = 'kyrsova.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'kyrsova/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'kyrsova.context_processors.add_user_profile_to_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'kyrsova.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
<<<<<<< HEAD
    'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=1800)
=======
    'default': { 
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'railway', 
        'USER': 'root', 
        'PASSWORD': 'kKMtYqiuPzmypLCpWKhXdciMgeDUaRhU', 
        'HOST': 'viaduct.proxy.rlwy.net', 
        'PORT': '51971' 
    }
>>>>>>> origin/main
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

LANGUAGE_CODE = 'uk'

TIME_ZONE = 'Europe/Kiev'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'kyrsova/static')
]
STATIC_ROOT =os.path.join(BASE_DIR, 'staticfiles')

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'foodzero.restaurant@gmail.com'
EMAIL_HOST_PASSWORD = 'vxmi rrsw wfil mifa'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

LOCALE_PATHS = ( os.path.join(BASE_DIR, 'locale'), )
