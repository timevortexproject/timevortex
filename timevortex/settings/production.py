#!/usr/bin/python3
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""settings.py"""

from timevortex.settings.base import *  # noqa

#####
# Logging configuration
#
LOG_BASE_FOLDER = '../common/log'
LOGGING['handlers']['file']['filename'] = '%s/timevortex.log' % LOG_BASE_FOLDER  # noqa
LOGGING['handlers']['file_weather']['filename'] = '%s/timevortex_weather.log' % LOG_BASE_FOLDER  # noqa
LOGGING['handlers']['file_energy']['filename'] = '%s/timevortex_energy.log' % LOG_BASE_FOLDER  # noqa
LOGGING['loggers']['timevortex']['level'] = 'INFO'  # noqa
LOGGING['loggers']['weather']['level'] = 'INFO'  # noqa
LOGGING['loggers']['energy']['level'] = 'INFO'  # noqa

#####
# Timevortex configuration
#

SETTINGS_FILE_STORAGE_FOLDER = '../common/data'

#####
# Email configuration
#

DEFAULT_FROM_EMAIL = 'Timevortex <XXX@XXX.com>'
EMAIL_HOST = 'XXX.XXX.XXX'
EMAIL_HOST_USER = 'XXX'
EMAIL_HOST_PASSWORD = 'XXX'  # noqa
EMAIL_PORT = 587
EMAIL_USE_TLS = True

#####
# BACKUP CONFIGURATION
#

BACKUP_TARGET_FOLDER = None

#####
# DATABASE CONFIGURATION
#

DATABASES['default']['NAME'] = '../common/db.sqlite3'  # noqa
