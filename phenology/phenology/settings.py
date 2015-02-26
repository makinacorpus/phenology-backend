#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

"""
Django settings for phenology-backend project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

from django.utils.translation import gettext_lazy as _


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'c9r!po=exbp_=p%uu&bm6hb*0z8brm#)9b_fy-t0+!=k0(e3mk'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Application definition
ACCOUNT_ACTIVATION_DAYS = 7
# One-week activation window; you may, of course, use a different value.

INSTALLED_APPS = (
    'south',  # improve migration
    'backend',  # backend with model + rest
    'backoffice',  # backoffice with forms
    'phenology',  # settings
    'bootstrap3',  # boostrap3 integration
    'select2',  # allow to use select2 field at model level
    'modeltranslation',  # allow to translate model field
    'rest_framework',  # Rest api
    'registration',
    'registration_defaults',
    'corsheaders',  # server headers required for Cross-Origin Resource Sharing
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'easy_thumbnails',
    'compressor'
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
    'django.core.context_processors.i18n'
)

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

# Default settings
BOOTSTRAP3 = {
    'horizontal_label_class': 'col-md-3',
    'horizontal_field_class': 'col-md-8',
}

ROOT_URLCONF = 'phenology.urls'

WSGI_APPLICATION = 'phenology.wsgi.application'

# SITE_SUPERUSER_ID = '343'
# SITE_SUPERUSER_USERNAME = 'admin'
# SITE_SUPERUSER_EMAIL = 'myadmin@example.com'
# SITE_SUPERUSER_PASSWORD = 'admin'  # this can be set from a secret file.

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated', ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
    )
}
DATE_FORMAT = 'iso-8601'
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

#LANGUAGE_CODE = 'fr'

LANGUAGES = (
    ('fr', _('french')),
    ('it', _('italian')),
    ('en', _('english'))
)
#AUTH_USER_MODEL = 'backend.Observer'

TIME_ZONE = 'Europe/Paris'
LANGUAGE_CODE = 'fr'
SITE_ID = 1
DEFAULT_LANGUAGE = 1
USE_I18N = True
USE_L10N = True
#USE_TZ = True


LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

CORS_ORIGIN_ALLOW_ALL = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, "static_root")
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
STATIC_URL = '/static/'

TILES_SETTINGS = {
    'TILES_RADIUS_LARGE': 0.01,  # ~1 km
    'TILES_RADIUS_SMALL': 0.05,  # ~500 m
    'TILES_GLOBAL_ZOOMS': range(5, 11),  # zoom 7 to 10
    'TILES_AREA_ZOOMS': range(11, 17),  # zoom 11 to 16
    'TILES_ROOT': os.path.join(MEDIA_ROOT, 'tiles'),
    'TILES_URL': 'http://{s}.tile.thunderforest.com/landscape/{z}/{x}/{y}.png',  # tiles url
    'GLOBAL_MAP_BBOX': [4.669189453125, 43.69965122967144, 7.9046630859375, 46.464349400461124],  # Whole Alpes
}

THUMBNAIL_ALIASES = {
    '': {
        'thumbnail': {'size': (100, 100), 'crop': 'smart', 'quality': 100},
        'thumbnail_2x': {'size': (200, 200), 'crop': 'smart', 'quality': 100},
        'mobile': {'size': (640, 960)},
        'mobile_2x': {'size': (1280, 1260)},
        'tablet': {'size': (1024, 768)},
        'tablet_2w': {'size': (2048, 768)}
    },
}

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django': {
            'handlers': ['console', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'backend': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
            'propagate': False,
        },
        'landez': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
            'propagate': False,
        },
        '': {
            'handlers': ['console', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}

try:
    from .settings_local import *
except ImportError:
    pass

