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
ERROR_MISSING_SENDER_EMAIL = "error_missing_sender_email"
ERROR_SMTP_AUTH = "error_smtp_authentication"
ERROR_MISSING_SENDER_PASSWORD = "error_missing_sender_password"  # noqa
ERROR_MISSING_TARGET_EMAIL = "error_missing_target_email"
KEY_SENDER_EMAIL = "sender_email"
KEY_SENDER_PASSWORD = "sender_password"  # noqa
KEY_TARGET_INFORMATION_EMAIL = "target_information_email"
KEY_NEXT_SEND_DAILY_REPORT = "next_send_daily_report"
KEY_LAST_TIME_DAILY_REPORT = "last_time_daily_report"
ERROR_MISSING_NEXT_SEND = "error_missing_next_send"
KEY_EMAIL_HOST_USER = "EMAIL_HOST_USER"
KEY_EMAIL_HOST_PASSWORD = "EMAIL_HOST_PASSWORD"  # noqa
KEY_MISSING_DB_ELEMENT = "Missing %s in DB."
LABEL_LAST_TIME_DAILY_REPORT = "Last time daily report"
ERROR_TIMEVORTEX = {
    ERROR_BACKUP_DEACTIVATED: "Backup script deactivated. Please specify target destination to activate the command.",
    ERROR_SMTP_AUTH: "Error with SMTP authentication, verify that %s and %s are correct",
    ERROR_MISSING_SENDER_EMAIL: KEY_MISSING_DB_ELEMENT % KEY_SENDER_EMAIL,
    ERROR_MISSING_SENDER_PASSWORD: KEY_MISSING_DB_ELEMENT % KEY_SENDER_PASSWORD,
    ERROR_MISSING_TARGET_EMAIL: KEY_MISSING_DB_ELEMENT % KEY_TARGET_INFORMATION_EMAIL,
    ERROR_MISSING_NEXT_SEND: KEY_MISSING_DB_ELEMENT % KEY_NEXT_SEND_DAILY_REPORT,
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
