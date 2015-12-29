#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""Functionnal test for timeserieslogger"""

import json
from time import sleep
from behave import when
from io import StringIO
from timevortex.utils.commands import AbstractCommand
from features.steps.test_utils import DICT_TSL_ERROR_DATA, reset_testing_environment
from timevortex.utils.globals import LOGGER


@when("I send JSON message '{error_type}'")
def sending_json_message(context, error_type):
    reset_testing_environment()
    out = StringIO()
    command = AbstractCommand()
    command.out = out
    if DICT_TSL_ERROR_DATA[error_type] is not None:
        command.timeseries = DICT_TSL_ERROR_DATA[error_type]
        context.specific_error = json.dumps(command.timeseries)
    command.send_timeseries()
    context.commands_response = [out.getvalue().strip()]
    LOGGER.info("End of sending json message")
    sleep(1)
