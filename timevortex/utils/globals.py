#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""Globals"""

import logging

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
