#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""settings.py"""

from timevortex.settings.base import *  # noqa

#####
# Logging configuration
#
LOG_BASE_FOLDER = "/tmp/timevortex"
LOGGING['handlers']['file']['filename'] = '%s/timevortex.log' % LOG_BASE_FOLDER
LOGGING['handlers']['file_weather']['filename'] = '%s/timevortex_weather.log' % LOG_BASE_FOLDER
LOGGING['handlers']['file_energy']['filename'] = '%s/timevortex_energy.log' % LOG_BASE_FOLDER
LOGGING['loggers']['timevortex']['level'] = 'DEBUG'
LOGGING['loggers']['weather']['level'] = 'DEBUG'
LOGGING['loggers']['energy']['level'] = 'DEBUG'

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