#!/usr/bin/python3
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""Globals"""

import logging
from time import tzname
from subprocess import call

SYSTEM_SITE_ID = "system"
LOGGER = logging.getLogger("timevortex")
KEY_SITE_ID = "siteID"
KEY_VARIABLE_ID = "variableID"
KEY_VALUE = "value"
KEY_DATE = "date"
KEY_DST_TIMEZONE = "dstTimezone"
KEY_NON_DST_TIMEZONE = "nonDstTimezone"
KEY_ERROR = "error"
KEY_TIMESERIES = "timeseries"
ERROR_TIMESERIES_NOT_DEFINED = "self.timeseries does not exist. Please create one before send any message."
ERROR_BACKUP_DEACTIVATED = "error_backup_deactivated"
ERROR_TIMEVORTEX = {
    ERROR_BACKUP_DEACTIVATED: "Backup script deactivated. Please specify a target destination to activate the command."
}


def timeseries_json(site_id, variable_id, value, date):
    """Create a TimeVortex json format dict
    """
    return {
        KEY_SITE_ID: site_id,
        KEY_VARIABLE_ID: variable_id,
        KEY_VALUE: value,
        KEY_DATE: date,
        KEY_DST_TIMEZONE: tzname[1],
        KEY_NON_DST_TIMEZONE: tzname[0]
    }


def call_and_exit(command, shell=True):
    """Call a shell command and exit if error
    """
    code = call(command, shell=shell)
    if code != 0:
        exit(1)
