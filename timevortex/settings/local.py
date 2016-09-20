#!/usr/bin/python3
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""settings.py"""

from timevortex.settings.base import *  # noqa

#####
#
#

INSTALLED_APPS += [  # noqa
    'django_nose',
    'behave_django',
]

#####
# Logging configuration
#
LOG_BASE_FOLDER = "/tmp/timevortex"
LOGGING['handlers']['file']['filename'] = '%s/timevortex.log' % LOG_BASE_FOLDER  # noqa
LOGGING['handlers']['file_weather']['filename'] = '%s/timevortex_weather.log' % LOG_BASE_FOLDER  # noqa
LOGGING['handlers']['file_energy']['filename'] = '%s/timevortex_energy.log' % LOG_BASE_FOLDER  # noqa
LOGGING['loggers']['timevortex']['level'] = 'DEBUG'  # noqa
LOGGING['loggers']['weather']['level'] = 'DEBUG'  # noqa
LOGGING['loggers']['energy']['level'] = 'DEBUG'  # noqa

#####
# Timevortex configuration
#

SETTINGS_FILE_STORAGE_FOLDER = "/tmp/data"

#####
# Email configuration
#

DEFAULT_FROM_EMAIL = 'Timevortex <phase.test.email@gmail.com>'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'phase.test.email'
EMAIL_HOST_PASSWORD = 'phaseTEST2014'  # noqa
EMAIL_PORT = 587
EMAIL_USE_TLS = True

#####
# BACKUP CONFIGURATION
#

BACKUP_TARGET_FOLDER = "/tmp/backup"
