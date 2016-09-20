#!/usr/bin/python3
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""TSL functions"""

from timevortex.utils.globals import ERROR_TIMESERIES_NOT_DEFINED

KEY_TSL_BAD_JSON = "ts_without_json_message"
KEY_TSL_NO_SITE_ID = "ts_without_site_id"
KEY_TSL_NO_VARIABLE_ID = "ts_without_variable_id"
KEY_TSL_NO_VALUE = "ts_without_message"
KEY_TSL_NO_DATE = "ts_without_date"
KEY_TSL_NO_DST_TIMEZONE = "ts_without_dst_timezone"
KEY_TSL_NO_NON_DST_TIMEZONE = "ts_without_non_dst_timezone"
INCORRECT_MESSAGE = "Receive incorrect message => %s"
ERROR_TSL = {
    KEY_TSL_BAD_JSON: ERROR_TIMESERIES_NOT_DEFINED,
    KEY_TSL_NO_SITE_ID: INCORRECT_MESSAGE % "missing siteID in %s",
    KEY_TSL_NO_VARIABLE_ID: INCORRECT_MESSAGE % "missing variableID in %s",
    KEY_TSL_NO_VALUE: INCORRECT_MESSAGE % "missing value in %s",
    KEY_TSL_NO_DATE: INCORRECT_MESSAGE % "missing date in %s",
    KEY_TSL_NO_DST_TIMEZONE: INCORRECT_MESSAGE % "missing dstTimezone in %s",
    KEY_TSL_NO_NON_DST_TIMEZONE: INCORRECT_MESSAGE % "missing nonDstTimezone in %s",
}
