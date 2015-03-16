#!/usr/bin/env python
# -*- coding: utf-8 -*-
__docformat__ = 'restructuredtext en'
{% set cfg = salt['mc_utils.json_load'](cfg) %}
{% set data = cfg.data %}
{% macro renderbool(opt)%}
{{opt}} = {%if data.get(opt, False)%}True{%else%}False{%endif%}
{% endmacro %}
import json
import os
from django.utils.translation import gettext_lazy as _
SITE_ID={{data.SITE_ID}}
SERVER_EMAIL = DEFAULT_FROM_EMAIL = 'root@{{cfg.fqdn}}'
DATABASES = json.loads("""
{{salt['mc_utils.json_dump'](data.db)}}
""".strip())
{% set admint = None %}
ADMINS = (
    {% for dadmins in data.admins %}
    {% for admin, data in dadmins.items() %}
    {% if data %}{% set admint = (admin, data) %}{%endif %}
    ('{{admin}}', '{{data.mail}}'),
    {% endfor %}
    {% endfor %}
)
{{renderbool('DEBUG') }}
{% for i in data.server_aliases %}
{% if i not in data.ALLOWED_HOSTS %}
{% do data.ALLOWED_HOSTS.append(i) %}
{% endif %}
{% endfor %}
CORS_ORIGIN_ALLOW_ALL = {{data.CORS_ORIGIN_ALLOW_ALL}}
ALLOWED_HOSTS = {{data.ALLOWED_HOSTS}}
DEFAULT_FROM_EMAIL = '{{data.adminmail}}'
MEDIA_ROOT = '{{data.media}}'
STATIC_ROOT = '{{data.static}}'
SECRET_KEY = '{{data.SECRET_KEY}}'
USE_X_FORWARDED_HOST={{data.USE_X_FORWARDED_HOST}}
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
DATE_FORMAT = '{{data.DATE_FORMAT}}'
TIME_ZONE = '{{data.timezone}}'
LANGUAGE_CODE = '{{data.LANGUAGE_CODE}}'
LANGUAGES = (
    ('fr', _('Français')),
    ('it', _('Italia')),
    ('en', _('English'))
)
TILES_SETTINGS = {
    'TILES_RADIUS_LARGE': 0.01,  # ~1 km
    'TILES_RADIUS_SMALL': 0.05,  # ~500 m
    'TILES_GLOBAL_ZOOMS': range(5, 11),  # zoom 7 to 10
    'TILES_AREA_ZOOMS': range(11, 17),  # zoom 11 to 16
    'TILES_ROOT': os.path.join(MEDIA_ROOT, 'tiles'),
    'TILES_URL': 'http://{s}.tile.thunderforest.com/landscape/{z}/{x}/{y}.png',  # tiles url
    'GLOBAL_MAP_BBOX': [4.669189453125, 43.69965122967144, 7.9046630859375, 46.464349400461124],  # Whole Alpes
}
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
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console', 'mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django': {
            'handlers': ['console', 'mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        }
    }
}
{% if data.get('ADDITIONAL_TEMPLATE_DIRS', None) %}
ADDITIONAL_TEMPLATE_DIRS = tuple({{data.ADDITIONAL_TEMPLATE_DIRS}})
{% endif %}

EMAIL_HOST = '{{data.EMAIL_HOST}}'
EMAIL_HOST_USER = '{{data.EMAIL_HOST_USER}}'
EMAIL_HOST_PASSWORD = '{{data.EMAIL_HOST_PASSWORD}}'
EMAIL_PORT = '{{data.EMAIL_PORT}}'
EMAIL_USE_TLS = '{{data.EMAIL_USE_TLS}}'

# Application specific settings
{% for param, value in data.get('extra_settings', {}).items() %}
{{param}} = {{value}}
{% endfor %}
# vim:set et sts=4 ts=4 tw=80:



