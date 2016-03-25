#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""Functionnal test for timeserieslogger"""

import json
from time import sleep, tzname
from io import StringIO
from behave import when  # pylint: disable=I0011,E0611
from timevortex.utils.commands import AbstractCommand
from timevortex.utils.timeserieslogger import KEY_TSL_NO_NON_DST_TIMEZONE
from timevortex.utils.timeserieslogger import KEY_TSL_NO_VALUE, KEY_TSL_NO_DATE, KEY_TSL_NO_DST_TIMEZONE
from timevortex.utils.timeserieslogger import KEY_TSL_BAD_JSON, KEY_TSL_NO_SITE_ID, KEY_TSL_NO_VARIABLE_ID
from timevortex.utils.globals import LOGGER
from timevortex.utils.globals import KEY_SITE_ID, KEY_VARIABLE_ID, KEY_VALUE, KEY_DATE, KEY_DST_TIMEZONE
from timevortex.utils.globals import KEY_NON_DST_TIMEZONE, KEY_ERROR
from features.steps.test_globals import reset_testing_environment
from features.steps.currentcost import TEST_CC_SITE_ID, TEST_CC_VARIABLE_ID_WATTS_CH2, TEST_CC_VARIABLE_ID_KWH_CH2
from features.steps.currentcost import TEST_CC_VARIABLE_ID_TMPR


DICT_TSL_ERROR_DATA = {
    KEY_TSL_BAD_JSON: None,
    KEY_TSL_NO_SITE_ID: {
        KEY_VARIABLE_ID: "sdsqdsqd",
        KEY_DATE: "12",
        KEY_VALUE: "sdsqdf",
        KEY_DST_TIMEZONE: "qsdfqsd",
        KEY_NON_DST_TIMEZONE: "sdfsdfzs",
    },
    KEY_TSL_NO_VARIABLE_ID: {
        KEY_SITE_ID: "sqdfsqg",
        KEY_DATE: "12",
        KEY_VALUE: "sdsqdf",
        KEY_DST_TIMEZONE: "qsdfqsd",
        KEY_NON_DST_TIMEZONE: "sdfsdfzs",
    },
    KEY_TSL_NO_VALUE: {
        KEY_SITE_ID: "sqdfsqg",
        KEY_VARIABLE_ID: "sdsqdsqd",
        KEY_DATE: "12",
        KEY_DST_TIMEZONE: "qsdfqsd",
        KEY_NON_DST_TIMEZONE: "sdfsdfzs",
    },
    KEY_TSL_NO_DATE: {
        KEY_SITE_ID: "sqdfsqg",
        KEY_VARIABLE_ID: "sdsqdsqd",
        KEY_VALUE: "sdsqdf",
        KEY_DST_TIMEZONE: "qsdfqsd",
        KEY_NON_DST_TIMEZONE: "sdfsdfzs",
    },
    KEY_TSL_NO_DST_TIMEZONE: {
        KEY_SITE_ID: "sqdfsqg",
        KEY_VARIABLE_ID: "sdsqdsqd",
        KEY_DATE: "12",
        KEY_VALUE: "sdsqdf",
        KEY_NON_DST_TIMEZONE: "sdfsdfzs",
    },
    KEY_TSL_NO_NON_DST_TIMEZONE: {
        KEY_SITE_ID: "sqdfsqg",
        KEY_VARIABLE_ID: "sdsqdsqd",
        KEY_DATE: "12",
        KEY_VALUE: "sdsqdf",
        KEY_DST_TIMEZONE: "qsdfqsd",
    },
    "ts_error_message": {
        KEY_SITE_ID: TEST_CC_SITE_ID,
        KEY_VARIABLE_ID: KEY_ERROR,
        KEY_DATE: "2015-12-26T22:00:00.000000+00:00",
        KEY_VALUE: "Basic error that you should avoid.",
        KEY_DST_TIMEZONE: tzname[1],
        KEY_NON_DST_TIMEZONE: tzname[0],
    },
    "ts_first_watts": {
        KEY_SITE_ID: TEST_CC_SITE_ID,
        KEY_VARIABLE_ID: TEST_CC_VARIABLE_ID_WATTS_CH2,
        KEY_DATE: "2015-12-27T22:00:00.000000+00:00",
        KEY_VALUE: "350",
        KEY_DST_TIMEZONE: tzname[1],
        KEY_NON_DST_TIMEZONE: tzname[0],
    },
    "ts_first_kwh": {
        KEY_SITE_ID: TEST_CC_SITE_ID,
        KEY_VARIABLE_ID: TEST_CC_VARIABLE_ID_KWH_CH2,
        KEY_DATE: "2015-12-27T22:00:00.000000+00:00",
        KEY_VALUE: "0.00254",
        KEY_DST_TIMEZONE: tzname[1],
        KEY_NON_DST_TIMEZONE: tzname[0],
    },
    "ts_first_temperature": {
        KEY_SITE_ID: TEST_CC_SITE_ID,
        KEY_VARIABLE_ID: TEST_CC_VARIABLE_ID_TMPR,
        KEY_DATE: "2015-12-27T22:00:00.000000+00:00",
        KEY_VALUE: "25.3",
        KEY_DST_TIMEZONE: tzname[1],
        KEY_NON_DST_TIMEZONE: tzname[0],
    },
    "ts_second_watts": {
        KEY_SITE_ID: TEST_CC_SITE_ID,
        KEY_VARIABLE_ID: TEST_CC_VARIABLE_ID_WATTS_CH2,
        KEY_DATE: "2015-12-28T22:00:00.000000+00:00",
        KEY_VALUE: "2458",
        KEY_DST_TIMEZONE: tzname[1],
        KEY_NON_DST_TIMEZONE: tzname[0],
    },
    "ts_second_kwh": {
        KEY_SITE_ID: TEST_CC_SITE_ID,
        KEY_VARIABLE_ID: TEST_CC_VARIABLE_ID_KWH_CH2,
        KEY_DATE: "2015-12-28T22:00:00.000000+00:00",
        KEY_VALUE: "1.02356",
        KEY_DST_TIMEZONE: tzname[1],
        KEY_NON_DST_TIMEZONE: tzname[0],
    },
    "ts_second_temperature": {
        KEY_SITE_ID: TEST_CC_SITE_ID,
        KEY_VARIABLE_ID: TEST_CC_VARIABLE_ID_TMPR,
        KEY_DATE: "2015-12-28T22:00:00.000000+00:00",
        KEY_VALUE: "11.5",
        KEY_DST_TIMEZONE: tzname[1],
        KEY_NON_DST_TIMEZONE: tzname[0],
    },
}


@when("I send JSON message '{error_type}'")
def sending_json_message(context, error_type):
    """Sending JSON messages
    """
    reset_testing_environment()
    out = StringIO()
    command = AbstractCommand()
    command.out = out
    command.set_logger(LOGGER)
    if DICT_TSL_ERROR_DATA[error_type] is not None:
        command.timeseries = DICT_TSL_ERROR_DATA[error_type]
        context.specific_error = json.dumps(command.timeseries)
    command.send_timeseries()
    context.commands_response = [out.getvalue().strip()]
    LOGGER.info("End of sending json message")
    sleep(1)
