#!/usr/bin/python3
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""Functionnal test toolkit"""

import os
import json
import shlex
import signal
import requests
import subprocess
from time import sleep
from io import StringIO
from behave import given, when, then
from timevortex.models import Site, create_site
from timevortex.utils.globals import LOGGER
from features.steps.test_globals import KEY_LABEL, KEY_SITE_TYPE, WITH_STUBS, DICT_JSON_REQUEST_HEADER, assert_equal
from features.steps.test_globals import read_log, TIMEVORTEX_LOG_FILE, STUBS_COMMAND, reset_testing_environment
from features.steps.currentcost import TIMEVORTEX_CURRENTCOST_LOG_FILE
from features.steps.currentcost import CC_INSTANT_CONSO_1_TS_0, CC_INSTANT_CONSO_1_TS_3, CC_INSTANT_CONSO_2_TS_7
from features.steps.currentcost import CC_INSTANT_CONSO_2_TS_3, CC_INSTANT_CONSO_2_TS_0, CC_INSTANT_CONSO_3_TS_3
from features.steps.currentcost import CURRENTCOST_MESSAGE, CURRENTCOST_MESSAGE_2, CURRENTCOST_MESSAGE_3
from features.steps.currentcost import launch_currentcost_command, DICT_CC_DATA_TYPE, verify_currentcost_tsv_update
from features.steps.currentcost import verify_currentcost_data_update, CC_HISTORY, HISTORY_1
from features.steps.metear import KEY_WEATHER_LOG_FILE, TIMEVORTEX_WEATHER_LOG_FILE, launch_metear_command
from features.steps.metear import verify_metear_data_update, verify_metear_tsv_update, KEY_METEAR
from features.steps.metear import TEST_METEAR_LABEL, TEST_METEAR_SITE_ID, TEST_METEAR_LABEL_2, TEST_METEAR_SITE_ID_2
from features.steps.currentcost import TEST_CC_LABEL, TEST_CC_SITE_ID
from stubs.utils.globals import URL_STUBS_CHANGE_ROUTE_CONFIG, KEY_STUBS_OPEN_METEAR_API
from energy.utils.globals import ERROR_CURRENTCOST, KEY_CURRENTCOST
from weather.utils.globals import ERROR_METEAR
from timevortex.utils.timeserieslogger import ERROR_TSL
from timevortex.utils.globals import ERROR_TIMEVORTEX
from timevortex.utils.globals import KEY_SITE_ID, KEY_VARIABLE_ID, KEY_VALUE, KEY_DATE, KEY_DST_TIMEZONE
from timevortex.utils.globals import KEY_NON_DST_TIMEZONE, SYSTEM_SITE_ID
from timevortex.utils.filestorage import FILE_STORAGE_SPACE

DICT_SITE = {
    TEST_METEAR_SITE_ID: {KEY_LABEL: TEST_METEAR_LABEL, KEY_SITE_TYPE: Site.METEAR_TYPE, WITH_STUBS: True},
    TEST_METEAR_SITE_ID_2: {KEY_LABEL: TEST_METEAR_LABEL_2, KEY_SITE_TYPE: Site.METEAR_TYPE, WITH_STUBS: True},
    TEST_CC_SITE_ID: {KEY_LABEL: TEST_CC_LABEL, KEY_SITE_TYPE: Site.HOME_TYPE, WITH_STUBS: False},
}


def error_list(array_dict):
    error_list = {}
    for error_dict in array_dict:
        for key in error_dict:
            error_list[key] = error_dict[key]
    return error_list


ERROR_LIST = error_list([ERROR_METEAR, ERROR_TSL, ERROR_CURRENTCOST, ERROR_TIMEVORTEX])


def error_in_list(error_type, duplicate=False):
    if error_type in ERROR_LIST:
        return ERROR_LIST[error_type]


def stubs_change_api_configuration(config):
    requests.post(
        URL_STUBS_CHANGE_ROUTE_CONFIG,
        json.dumps(config),
        headers=DICT_JSON_REQUEST_HEADER,
    )


def verify_json_message(json_message, expected_message):
    """
        Verify JSON message value.
    """
    LOGGER.debug(json_message)
    LOGGER.debug(expected_message)
    try:
        message = json.loads(json_message)
    except TypeError:
        message = json_message
    validation = [KEY_SITE_ID, KEY_VARIABLE_ID, KEY_VALUE, KEY_DATE, KEY_DST_TIMEZONE, KEY_NON_DST_TIMEZONE]
    for key in validation:
        assert_equal(message[key], expected_message[key])


def extract_from_log(expected_message, log_file_path, line):
    """
        Method that extract expecting line from log and compare
        to expected_message
    """
    body = read_log(log_file_path, line)

    try:
        verify_json_message(body, expected_message)
    except ValueError:
        assert_equal(expected_message, body)


def check_response_script(commands_response, error):
    """
        Launch script with parameter.
    """
    LOGGER.info(commands_response)
    for cmdr in commands_response:
        cmdr = cmdr.replace("\n", "")
        assert cmdr is not None, "%s should not equal to %s" % (cmdr, None)
        assert cmdr is not "", "%s should not equal to %s" % (cmdr, "")
        assert_equal(error, cmdr)


@given("I shutdown the metear web service")
def shutdown_metear_ws(context):
    stubs_change_api_configuration({KEY_STUBS_OPEN_METEAR_API: False})


def define_cc_error_message(error_type):
    """Define currentcost error
    """
    error = None
    if error_type in [CC_INSTANT_CONSO_1_TS_0, CC_INSTANT_CONSO_1_TS_3]:
        error = CURRENTCOST_MESSAGE
    elif error_type in [CC_INSTANT_CONSO_2_TS_7, CC_INSTANT_CONSO_2_TS_3, CC_INSTANT_CONSO_2_TS_0]:
        error = CURRENTCOST_MESSAGE_2
    elif error_type in CC_INSTANT_CONSO_3_TS_3:
        error = CURRENTCOST_MESSAGE_3
    elif error_type in CC_HISTORY:
        error = HISTORY_1
    return error


@then("I should see an error message '{error_type}' in the '{log_file}' log")
def verify_error_message_on_log(context, error_type, log_file):
    error = error_in_list(error_type)
    # print(error)
    try:
        error = error % context.specific_error
    except AttributeError:
        pass
    log_file_path = TIMEVORTEX_LOG_FILE
    if log_file == KEY_WEATHER_LOG_FILE:
        log_file_path = TIMEVORTEX_WEATHER_LOG_FILE
    elif log_file == KEY_CURRENTCOST:
        log_file_path = TIMEVORTEX_CURRENTCOST_LOG_FILE

    cc_error = define_cc_error_message(error_type)
    if cc_error is not None:
        error = cc_error

    extract_from_log(error, log_file_path, -2)


@then("I should see an error message '{error_type}' on '{tsv_file_type}' TSV file")
def verify_error_message_on_system_tsv_file(context, error_type, tsv_file_type):
    error = error_in_list(error_type)
    try:
        error = error % context.specific_error
    except AttributeError:
        pass
    if SYSTEM_SITE_ID in tsv_file_type:
        last_error = FILE_STORAGE_SPACE.get_last_error(tsv_file_type)
    else:
        last_error = FILE_STORAGE_SPACE.get_last_error(context.site_id)
    assert_equal(error, last_error[KEY_VALUE])


@then("I should see an error message '{error_type}' on the screen")
def verify_error_message_on_screen(context, error_type):
    error = error_in_list(error_type)
    try:
        error = error % context.specific_error
    except AttributeError:
        pass
    check_response_script(context.commands_response, error)


@given("I created a testing Site '{site_id}'")
def create_testing_site(context, site_id):
    LOGGER.debug("Start creation site")
    reset_testing_environment()
    create_site(slug=site_id, label=DICT_SITE[site_id][KEY_LABEL], site_type=DICT_SITE[site_id][KEY_SITE_TYPE])
    context.site_id = site_id
    if DICT_SITE[site_id][WITH_STUBS] is True:
        commands = STUBS_COMMAND
        context.stubs = subprocess.Popen(shlex.split(commands), stdout=subprocess.PIPE, preexec_fn=os.setsid)
        sleep(3)
        stubs_change_api_configuration({KEY_STUBS_OPEN_METEAR_API: True})


def launch_correct_script(script_name, out, context, setting_type):
    """Launch correct script
    """
    if script_name in KEY_METEAR:
        launch_metear_command(out)
    if script_name in KEY_CURRENTCOST:
        launch_currentcost_command(out, context, setting_type)


@when("I run the '{script_name}' script with '{setting_type}' settings")
def run_script(context, script_name, setting_type):
    out = StringIO()
    launch_correct_script(script_name, out, context, setting_type)
    context.commands_response = [out.getvalue().strip()]

    try:
        os.killpg(context.stubs.pid, signal.SIGTERM)
    except AttributeError:
        pass

    try:
        os.killpg(context.socat.pid, signal.SIGTERM)
    except AttributeError:
        pass

    try:
        context.thread.join()
    except AttributeError:
        pass

    sleep(1)


@then("I should see '{data_type}' data update in DB for '{site_id}'")
def verify_data_update_db(context, data_type, site_id):
    if data_type in ["new", "historical"]:
        verify_metear_data_update(site_id, data_type)
    elif data_type in DICT_CC_DATA_TYPE:
        verify_currentcost_data_update(site_id, data_type)
    else:
        assert_equal("Unknown datatype %s error" % data_type, False)


@then("I should see '{data_type}' data update in TSV file for '{site_id}'")
def verify_data_update_tsv_file(context, data_type, site_id):
    if data_type in DICT_CC_DATA_TYPE:
        verify_currentcost_tsv_update(site_id, data_type)
    else:
        try:
            expected_message = json.loads(context.specific_error)
            site_id = expected_message[KEY_SITE_ID]
            variable_id = expected_message[KEY_VARIABLE_ID]
            last_series = FILE_STORAGE_SPACE.get_last_series(site_id, variable_id)
            verify_json_message(last_series, expected_message)
            return
        except AttributeError:
            verify_metear_tsv_update(site_id, data_type)
