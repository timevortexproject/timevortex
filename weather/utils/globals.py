#!/usr/bin/python3
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""Globals for weather app"""

from datetime import datetime, timedelta
from django.conf import settings

KEY_METEAR_NO_SITE_ID = "metear_no_site_id"
KEY_METEAR_BAD_URL = "metear_bad_url"
KEY_METEAR_PROBLEM_WS = "metear_problem_ws"
KEY_METEAR_BAD_CONTENT = "metear_bad_content"
KEY_METEAR_NO_START_DATE = "metear_no_start_date"
PROCESS_STOPPED = "Process stopped. Wait a minute before retrying."
ERROR_METEAR = {
    KEY_METEAR_NO_SITE_ID: "No METEAR Site in database. %s" % PROCESS_STOPPED,
    KEY_METEAR_BAD_URL: "Bad URL to target METEAR service. %s" % PROCESS_STOPPED,
    KEY_METEAR_PROBLEM_WS: "METEAR Web service does not respond. %s" % PROCESS_STOPPED,
    KEY_METEAR_BAD_CONTENT: "Bad content from METEAR Web service. %s" % PROCESS_STOPPED,
    KEY_METEAR_NO_START_DATE: "No start date found in DB. %s" % PROCESS_STOPPED,
}
SETTINGS_METEAR_URL = "METEAR_URL"
SETTINGS_DEFAULT_METEAR_URL = "http://www.wunderground.com/history/airport/%s/%s/DailyHistory.html?format=1"
SETTINGS_STUBS_METEAR_URL = "%s%s" % (settings.SITE_URL, "/stubs/history/airport/%s/%s/DailyHistory.html?format=1")
SETTINGS_STUBS_NEW_METEAR_URL = "%s%s" % (
    settings.SITE_URL, "/stubs/history/airport/%s/%s/NewDailyHistory.html?format=1")
SETTINGS_STUBS_METEAR_START_DATE = datetime.today() - timedelta(days=3)
