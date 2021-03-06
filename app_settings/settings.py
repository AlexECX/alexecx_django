"""
Django settings for banque_app project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^!(-5xxf8ecp9*qw7&l_ncm-zp+nz=mx8&xc*2igc6@rw4v@!6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

from alexecx_django.settings.base import *
from alexecx_django.settings.package import Settings as BaseSettings

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


ALLOWED_HOSTS += []


# Application definition

INSTALLED_APPS += BaseSettings.INSTALLED_APPS + [
]

TEMPLATES[0]['DIRS'] += BaseSettings.TEMPLATES[0].get('DIRS', [])



# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# DATABASES.update({
    # 'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
# })


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'fr_FR'

LANGUAGES += (
    ('fr', ugettext('french')),
    ('en', ugettext('english')),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'alexecx_django/locale'),
)

TIME_ZONE = 'Canada/Eastern'
