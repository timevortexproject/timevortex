#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""Globals"""

import logging
from time import tzname

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
