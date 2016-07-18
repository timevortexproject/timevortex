#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""settings.py"""

from timevortex.settings.base import *  # noqa

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
