#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""Functionnal test toolkit"""

import os
import json
import shlex
import shutil
import signal
import requests
import subprocess
from time import sleep
from io import StringIO
from time import tzname
from os.path import exists
from threading import Thread
from django.conf import settings
from behave import when, then
from datetime import datetime, timedelta
from timevortex.utils.globals import LOGGER
from stubs.utils.globals import URL_STUBS_CHANGE_ROUTE_CONFIG
from energy.utils.globals import KEY_CURRENTCOST, ERROR_CURRENTCOST, ERROR_CC_BAD_PORT, ERROR_CC_NO_MESSAGE
from energy.utils.globals import ERROR_CC_DISCONNECTED
from weather.management.commands.retrieve_metear_data import Command as MetearCommand
from energy.management.commands.retrieve_currentcost_data import Command as CurrentCostCommand
from weather.utils.globals import ERROR_METEAR, SETTINGS_STUBS_METEAR_URL, SETTINGS_METEAR_URL
from weather.utils.globals import SETTINGS_METEAR_START_DATE, SETTINGS_STUBS_METEAR_START_DATE
from timevortex.utils.timeserieslogger import KEY_TSL_NO_NON_DST_TIMEZONE
from timevortex.utils.timeserieslogger import KEY_TSL_NO_VALUE, KEY_TSL_NO_DATE, KEY_TSL_NO_DST_TIMEZONE
from timevortex.utils.timeserieslogger import ERROR_TSL, KEY_TSL_BAD_JSON, KEY_TSL_NO_SITE_ID, KEY_TSL_NO_VARIABLE_ID
from timevortex.utils.globals import KEY_SITE_ID, KEY_VARIABLE_ID, KEY_VALUE, KEY_DATE, KEY_DST_TIMEZONE
from timevortex.utils.globals import KEY_NON_DST_TIMEZONE, KEY_ERROR
from timevortex.utils.filestorage import SETTINGS_FILE_STORAGE_FOLDER, SETTINGS_DEFAULT_FILE_STORAGE_FOLDER
# import subprocess
# from subprocess import CalledProcessError
# Common
SOCAT = "socat"
TIMEVORTEX_LOG_FILE = "/tmp/timevortex.log"
DICT_JSON_REQUEST_HEADER = {'Content-type': 'application/json', 'Accept': '*/*'}
# Weather
TEST_METEAR_SITE_ID = "LFMN"
TEST_METEAR_SITE_ID_2 = "LFBP"
TEST_METEAR_LABEL = "Données METEAR de Nice, France"
TEST_METEAR_LABEL_2 = "Données METEAR de Pau, France"
SETTINGS_BAD_METEAR_URL = "http://ksgo/dsls/%s/hs/%s.shgdf"
SETTINGS_BAD_CONTENT_METEAR_URL = "%s%s" % (settings.SITE_URL, "/stubs/history/airport/%s/%s/badcontent.html?format=1")
TIMEVORTEX_WEATHER_LOG_FILE = "/tmp/timevortex_weather.log"
KEY_WEATHER_LOG_FILE = "weather"
KEY_METEAR = "metear"
KEY_METEAR_FAKE_DATA_ELEMENTS = "elements"
KEY_METEAR_FAKE_DATA_STATUS = "status"
KEY_METEAR_FAKE_DATA_DATE = "date"
KEY_METEAR_FAKE_DATA_OK = "ok"
KEY_METEAR_FAKE_DATA_KO = "ko"
DATE_METEAR_FAKE_DATA_TODAY = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
# Energy
TIMEVORTEX_CURRENTCOST_LOG_FILE = "/tmp/timevortex_energy.log"
TEST_CC_SITE_ID = "test_site"
TEST_CC_VARIABLE_ID = "test_variable"
TEST_CC_VARIABLE_ID_WATTS = "TEST_watts"
TEST_CC_VARIABLE_ID_KWH = "TEST_kwh"
TEST_CC_VARIABLE_ID_TMPR = "TEST_tmpr"
TEST_CC_CORRECT_TTY_PORT = "/tmp/tty_currentcost"
TEST_CC_CORRECT_TTY_PORT_WRITER = "/tmp/tty_currentcost_writer"
TEST_CC_BAD_TTY_PORT = "/tmp/tty_bad"
ERROR_UNDEFINED_ERROR_TYPE = "Undefined error_type %s"

DICT_METEAR_FAKE_DATA = [
    {
        KEY_METEAR_FAKE_DATA_DATE: (DATE_METEAR_FAKE_DATA_TODAY - timedelta(days=2, hours=8)).isoformat(" "),
        KEY_METEAR_FAKE_DATA_STATUS: KEY_METEAR_FAKE_DATA_OK,
        KEY_METEAR_FAKE_DATA_ELEMENTS: [
            "12:00 AM", "12", "6", "59", "1032", "15", "NNO", "11.1", "", "", "", "Assez nuageux", "330"]
    }, {
        KEY_METEAR_FAKE_DATA_DATE: (DATE_METEAR_FAKE_DATA_TODAY - timedelta(days=2, hours=8)).isoformat(" "),
        KEY_METEAR_FAKE_DATA_STATUS: KEY_METEAR_FAKE_DATA_KO,
        KEY_METEAR_FAKE_DATA_ELEMENTS: [
            "12:00 AM", "13.0", "7.0", "67", "1031", "10.0", "NO", "12.1", "-", "N/A", "", "Peu nuageux", "340"]
    }, {
        KEY_METEAR_FAKE_DATA_DATE: (DATE_METEAR_FAKE_DATA_TODAY - timedelta(days=2, hours=7)).isoformat(" "),
        KEY_METEAR_FAKE_DATA_STATUS: KEY_METEAR_FAKE_DATA_OK,
        KEY_METEAR_FAKE_DATA_ELEMENTS: [
            "13:00 AM", "12.5", "7.5", "67.5", "1031.5", "10.5", "N", "11.5", "-", "N/A", "", "Peu peu nuageux", "335"]
    }, {
        KEY_METEAR_FAKE_DATA_DATE: (DATE_METEAR_FAKE_DATA_TODAY + timedelta(hours=15)).isoformat(" "),
        KEY_METEAR_FAKE_DATA_STATUS: KEY_METEAR_FAKE_DATA_OK,
        KEY_METEAR_FAKE_DATA_ELEMENTS: [
            "12:30 AM", "14.0", "8.0", "68", "1030", "9.0", "O", "14.8", "-", "N/A", "", "Pas nuageux", "350"]
    }, {
        KEY_METEAR_FAKE_DATA_DATE: (DATE_METEAR_FAKE_DATA_TODAY + timedelta(hours=17)).isoformat(" "),
        KEY_METEAR_FAKE_DATA_STATUS: KEY_METEAR_FAKE_DATA_OK,
        KEY_METEAR_FAKE_DATA_ELEMENTS: [
            "1:00 AM", "15", "9", "57", "1033", "14", "S", "16.7", "", "", "", "Très nuageux", "320"]
    }, {
        KEY_METEAR_FAKE_DATA_DATE: (DATE_METEAR_FAKE_DATA_TODAY + timedelta(hours=17)).isoformat(" "),
        KEY_METEAR_FAKE_DATA_STATUS: KEY_METEAR_FAKE_DATA_KO,
        KEY_METEAR_FAKE_DATA_ELEMENTS: [
            "1:00 AM", "16", "10", "58", "1034", "13", "SO", "17.7", "", "", "", "Nuageux", "310"]
    }]

DICT_METEAR_FAKE_NEWS_DATA = [
    DICT_METEAR_FAKE_DATA[0],
    DICT_METEAR_FAKE_DATA[1],
    DICT_METEAR_FAKE_DATA[2],
    DICT_METEAR_FAKE_DATA[3],
    DICT_METEAR_FAKE_DATA[4],
    {
        KEY_METEAR_FAKE_DATA_DATE: (DATE_METEAR_FAKE_DATA_TODAY + timedelta(hours=19)).isoformat(" "),
        KEY_METEAR_FAKE_DATA_STATUS: KEY_METEAR_FAKE_DATA_OK,
        KEY_METEAR_FAKE_DATA_ELEMENTS: [
            "3:00 AM", "17", "11", "43", "1024", "9", "SSO", "8.3", "", "", "", "Ensoleillé", "180"]
    }, {
        KEY_METEAR_FAKE_DATA_DATE: (DATE_METEAR_FAKE_DATA_TODAY + timedelta(hours=19)).isoformat(" "),
        KEY_METEAR_FAKE_DATA_STATUS: KEY_METEAR_FAKE_DATA_KO,
        KEY_METEAR_FAKE_DATA_ELEMENTS: [
            "3:00 AM", "18.0", "12.0", "45", "1023", "12.0", "SSE", "8.5", "-", "N/A", "", "Bien ensoleillé", "150"]
    }]

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
        KEY_VARIABLE_ID: TEST_CC_VARIABLE_ID_WATTS,
        KEY_DATE: "2015-12-27T22:00:00.000000+00:00",
        KEY_VALUE: "350",
        KEY_DST_TIMEZONE: tzname[1],
        KEY_NON_DST_TIMEZONE: tzname[0],
    },
    "ts_first_kwh": {
        KEY_SITE_ID: TEST_CC_SITE_ID,
        KEY_VARIABLE_ID: TEST_CC_VARIABLE_ID_KWH,
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
        KEY_VARIABLE_ID: TEST_CC_VARIABLE_ID_WATTS,
        KEY_DATE: "2015-12-28T22:00:00.000000+00:00",
        KEY_VALUE: "2458",
        KEY_DST_TIMEZONE: tzname[1],
        KEY_NON_DST_TIMEZONE: tzname[0],
    },
    "ts_second_kwh": {
        KEY_SITE_ID: TEST_CC_SITE_ID,
        KEY_VARIABLE_ID: TEST_CC_VARIABLE_ID_KWH,
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


class SocatMessager(Thread):
    """Thread that send message over Socat."""

    def __init__(self, context, port, message=None):
        """Constructor"""
        Thread.__init__(self)
        self.context = context
        self.port = port
        self.message = message

    def run(self):
        """Main method."""
        sleep(1)

        if self.message is not None:
            ser = serial.Serial(self.port)
            ser.write("%s\n" % self.message)
            sleep(1)
            ser.close()
        else:
            try:
                os.killpg(self.context.socat.pid, signal.SIGTERM)
                sleep(1)
            except AttributeError:
                pass


def reset_testing_environment():
    data_folder = getattr(settings, SETTINGS_FILE_STORAGE_FOLDER, SETTINGS_DEFAULT_FILE_STORAGE_FOLDER)
    if exists(data_folder):
        shutil.rmtree(data_folder)
    setattr(settings, SETTINGS_METEAR_URL, SETTINGS_STUBS_METEAR_URL)
    setattr(settings, SETTINGS_METEAR_START_DATE, SETTINGS_STUBS_METEAR_START_DATE)


def assertEqual(element1, element2):
    try:
        assert element1 in element2, "%s should equal to %s" % (element1, element2)
    except TypeError:
        assert element1 == element2, "%s should equal to %s" % (element1, element2)


def error_list(array_dict):
    error_list = {}
    for error_dict in array_dict:
        for key in error_dict:
            error_list[key] = error_dict[key]
    return error_list


ERROR_LIST = error_list([ERROR_METEAR, ERROR_TSL, ERROR_CURRENTCOST])


def error_in_list(error_type, duplicate=False):
    if error_type in ERROR_LIST:
        return ERROR_LIST[error_type]


def transform_metear_array_into_dict(array):
    variables = {}
    variables["metear_temperature_celsius"] = array[1]
    variables["metear_dew_point_celsius"] = array[2]
    variables["metear_humidity_percentage"] = array[3]
    variables["metear_sea_level_pressure_hpa"] = array[4]
    variables["metear_visibility_km"] = array[5]
    variables["metear_wind_direction"] = array[6]
    variables["metear_wind_speed_kmh"] = array[7]
    variables["metear_gust_speed_kmh"] = array[8]
    variables["metear_precipitation_mm"] = array[9]
    variables["metear_events"] = array[10]
    variables["metear_conditions"] = array[11]
    variables["metear_wind_direction_degrees"] = array[12]
    return variables


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
        assertEqual(message[key], expected_message[key])


def read_log(log_file_path, line):
    log_file = open(log_file_path, "r")
    lines = log_file.readlines()
    log_file.close()
    body = lines[line]
    # log_message = "1. => %s" % body
    # LOGGER.debug(log_message)
    body = " ".join(body.split(" ")[9:])[:-1]
    # log_message = "2. => %s" % body
    # LOGGER.debug(log_message)
    return body


def counter_from_log(word, expected_occurency, log_file_path, line):
    from collections import Counter

    body = read_log(log_file_path, line)

    c = Counter()
    for line in body.splitlines():
        c.update(line.split())
    if expected_occurency == 0:
        assert word not in c, "%s should not be in %s" % (word, c)
    else:
        assert word in c, "%s should be in %s" % (word, c)
        assertEqual(c[word], expected_occurency)


def extract_from_log(expected_message, log_file_path, line):
    """
        Method that extract expecting line from log and compare
        to expected_message
    """
    body = read_log(log_file_path, line)

    try:
        verify_json_message(body, expected_message)
    except ValueError:
        assertEqual(body, expected_message)


def check_response_script(commands_response, error):
    """
        Launch script with parameter.
    """
    LOGGER.info(commands_response)
    for cmdr in commands_response:
        cmdr = cmdr.replace("\n", "")
        assert cmdr is not None, "%s should not equal to %s" % (cmdr, None)
        assert cmdr is not "", "%s should not equal to %s" % (cmdr, "")
        assertEqual(error, cmdr)


@when("I run the '{script_name}' script with '{setting_type}' settings")
def run_script(context, script_name, setting_type):
    out = StringIO()
    if script_name in KEY_METEAR:
        command = MetearCommand()
        command.out = out
        command.handle()
    if script_name in KEY_CURRENTCOST:
        commands = "%s PTY,link=%s PTY,link=%s" % (SOCAT, TEST_CC_CORRECT_TTY_PORT, TEST_CC_CORRECT_TTY_PORT_WRITER)
        context.socat = subprocess.Popen(shlex.split(commands), stdout=subprocess.PIPE, preexec_fn=os.setsid)
        tty_port = TEST_CC_CORRECT_TTY_PORT
        timeout = 10
        usb_retry = 1
        command = CurrentCostCommand()
        command.out = out
        if setting_type in ERROR_CC_BAD_PORT:
            tty_port = TEST_CC_BAD_TTY_PORT
            context.specific_error = (TEST_CC_VARIABLE_ID, TEST_CC_SITE_ID, tty_port, usb_retry)
        elif setting_type in ERROR_CC_NO_MESSAGE:
            timeout = 1
            context.specific_error = (TEST_CC_VARIABLE_ID, TEST_CC_SITE_ID)
        elif setting_type in ERROR_CC_DISCONNECTED:
            context.thread = SocatMessager(context, tty_port)
            context.thread.start()
        command.handle(
            site_id=TEST_CC_SITE_ID,
            variable_id=TEST_CC_VARIABLE_ID,
            tty_port=tty_port,
            timeout=timeout,
            usb_retry=usb_retry,
            break_loop=True)
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

@then("I should see an error message '{error_type}' in the '{log_file}' log")
def verify_error_message_on_log(context, error_type, log_file):
    error = error_in_list(error_type)
    try:
        error = error % context.specific_error
    except AttributeError:
        pass
    log_file_path = TIMEVORTEX_LOG_FILE
    if log_file == KEY_WEATHER_LOG_FILE:
        log_file_path = TIMEVORTEX_WEATHER_LOG_FILE
    elif log_file == KEY_CURRENTCOST:
        log_file_path = TIMEVORTEX_CURRENTCOST_LOG_FILE

    extract_from_log(error, log_file_path, -2)


@then("I should see an error message '{error_type}' on the screen")
def verify_error_message_on_screen(context, error_type):
    error = error_in_list(error_type)
    try:
        error = error % context.specific_error
    except AttributeError:
        pass 
    check_response_script(context.commands_response, error)


# @given("I created according settings for '{script_name}' to test '{error_type}'")
# def according_variable_creation(context, script_name, error_type):
#     if script_name in KEY_CURRENTCOST:
#         if error_type in MISSING_SITE_ID:
#             return
#         Site.objects.create(slug=TEST_HOME_SITE_ID, label=TEST_HOME_LABEL, site_type=Site.HOME_TYPE)
#         if error_type in MISSING_VARIABLE_ID:
#             return


# def launch_script(commands):
#     """
#         Launch script in a subprocess.
#     """
#     commands_response = []

#     for cmd in commands:
#         exception = None

#         try:
#             exception = subprocess.check_output(
#                 cmd, stderr=subprocess.STDOUT, shell=True)
#         except CalledProcessError as error:
#             exception = error

#         commands_response.append(exception)

#     return commands_response
