#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""Functionnal test for METEAR"""

import os
import signal
import json
from behave import given, when, then
from io import StringIO
from django.conf import settings
import subprocess
import shlex
from time import sleep
import requests
from features.steps.test_utils import check_response_script, extract_from_log
from features.steps.test_utils import TIMEVORTEX_LOG_FILE, TEST_METEAR_SITE_ID
from features.steps.test_utils import TEST_METEAR_LABEL, SETTINGS_BAD_METEAR_URL
from timevortex.models import Sites
from timevortex.utils.globals import LOGGER
from weather.utils.globals import ERROR_METEAR, SETTINGS_METEAR_URL, SETTINGS_STUBS_METEAR_URL
from weather.management.commands.retrieve_metear_data import Command
from stubs.utils.globals import KEY_STUBS_OPEN_METEAR_API, URL_STUBS_CHANGE_ROUTE_CONFIG

ERROR_UNDEFINED_ERROR_TYPE = "Undefined error_type %s"
STUBS_COMMAND = "python manage.py runserver 0.0.0.0:8000"
DICT_JSON_REQUEST_HEADER = {'Content-type': 'application/json', 'Accept': '*/*'}


@given("I created a testing Site")
def create_testing_site(context):
    setattr(settings, SETTINGS_METEAR_URL, SETTINGS_STUBS_METEAR_URL)
    Sites.objects.create(slug=TEST_METEAR_SITE_ID, label=TEST_METEAR_LABEL, site_type=Sites.METEAR_TYPE)
    sites = Sites.objects.all()
    LOGGER.debug(sites)

    commands = STUBS_COMMAND
    context.stubs = subprocess.Popen(shlex.split(commands), stdout=subprocess.PIPE, preexec_fn=os.setsid)

    sleep(3)


@given("I add a bad metear url in settings")
def define_wrong_metear_url(context):
    setattr(settings, SETTINGS_METEAR_URL, SETTINGS_BAD_METEAR_URL)


@given("I shutdown the metear web service")
def shutdown_metear_ws(context):
    requests.post(
        URL_STUBS_CHANGE_ROUTE_CONFIG,
        json.dumps({KEY_STUBS_OPEN_METEAR_API: False}),
        headers=DICT_JSON_REQUEST_HEADER,
    )


@when("I run the metear script")
def run_metear_script(context):
    out = StringIO()
    command = Command()
    command.out = out
    command.handle()
    context.commands_response = [out.getvalue().strip()]
    try:
        os.killpg(context.stubs.pid, signal.SIGTERM)
        sleep(1)
    except AttributeError:
        pass


@then("I should see an error message '{error_type}' in the log")
def verify_error_message_on_log(context, error_type):
    if error_type in ERROR_METEAR:
        error = ERROR_METEAR[error_type]
    else:
        assert False, ERROR_UNDEFINED_ERROR_TYPE % error_type
    extract_from_log(error, TIMEVORTEX_LOG_FILE, -1)


@then("I should see an error message '{error_type}' on the screen")
def verify_error_message_on_screen(context, error_type):
    if error_type in ERROR_METEAR:
        error = ERROR_METEAR[error_type]
    else:
        assert False, ERROR_UNDEFINED_ERROR_TYPE % error_type
    check_response_script(context.commands_response, error)
