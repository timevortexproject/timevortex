#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""settings.py"""

from timevortex.settings.base import *  # noqa

#####
# LOGGING
#

LOGGING['handlers']['file']['filename'] = '/var/log/timevortex/timevortex.log'
LOGGING['handlers']['file_weather']['filename'] = '/var/log/timevortex/timevortex_weather.log'
LOGGING['handlers']['file_energy']['filename'] = '/var/log/timevortex/timevortex_energy.log'

#####
# TIMEVORTEX CONFIGURATION
#

SETTINGS_FILE_STORAGE_FOLDER = "/opt/timevortex/data"

#####
# Email configuration
#

DEFAULT_FROM_EMAIL = 'Timevortex <XXX@XXX.com>'
EMAIL_HOST = 'XXX.XXX.XXX'
EMAIL_HOST_USER = 'XXX'
EMAIL_HOST_PASSWORD = 'XXX'  # noqa
EMAIL_PORT = 587
EMAIL_USE_TLS = True
