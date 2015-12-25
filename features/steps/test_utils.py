#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""Functionnal test toolkit"""

import json
from time import tzname
from timevortex.utils.globals import LOGGER
# import subprocess
# from subprocess import CalledProcessError

TEST_METEAR_SITE_ID = "LFMN"
TEST_METEAR_LABEL = "Données METEAR de Nice"
SETTINGS_BAD_METEAR_URL = "http://ksgo/dsls/%s/hs/%s.shgdf"
TIMEVORTEX_LOG_FILE = "/tmp/timevortex.log"


def verify_json_message(body, expected_message):
    """
        Verify JSON message value.
    """
    LOGGER.debug(body)
    message = json.loads(body)
    assert message["value"] == expected_message, "%s should equal to %s" % (
        message["value"], expected_message)
    assert message["siteID"] == TEST_METEAR_SITE_ID, "%s should equal to %s" % (
        message["siteID"], TEST_METEAR_SITE_ID)
    # assert message["variableID"] == DEVICE_ID, "%s should equal to %s" % (
    #     message["variableID"], DEVICE_ID)
    assert message["dstTimezone"] == tzname[1], "%s should equal to %s" % (
        message["dstTimezone"], tzname[1])
    assert message["nonDstTimezone"] == tzname[0], "%s should equal to %s" % (
        message["nonDstTimezone"], tzname[0])


def extract_from_log(expected_message, log_file_path, line):
    """
        Method that extract expecting line from log and compare
        to expected_message
    """
    log_file = open(log_file_path, "r")
    lines = log_file.readlines()
    log_file.close()
    body = lines[line]
    # log_message = "1. => %s" % body
    # LOGGER.debug(log_message)
    body = " ".join(body.split(" ")[9:])[:-1]
    # log_message = "2. => %s" % body
    # LOGGER.debug(log_message)

    try:
        verify_json_message(body, expected_message)
    except ValueError:
        assert body == expected_message, "%s is not equal to %s" % (
            body, expected_message)


def check_response_script(commands_response, error):
    """
        Launch script with parameter.
    """
    for cmdr in commands_response:
        cmdr = cmdr.replace("\n", "")
        assert cmdr is not None, "%s should not equal to %s" % (
            cmdr, None)
        assert cmdr is not "", "%s should not equal to %s" % (
            cmdr, "")
        assert cmdr in error, "%s should be in %s" % (
            cmdr, error)


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
