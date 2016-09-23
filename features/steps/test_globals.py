#!/usr/bin/python3
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""Functionnal test toolkit"""

import shutil
from os.path import exists
from django.conf import settings
from timevortex.utils.filestorage import SETTINGS_FILE_STORAGE_FOLDER, SETTINGS_DEFAULT_FILE_STORAGE_FOLDER
from weather.utils.globals import SETTINGS_STUBS_METEAR_URL, SETTINGS_METEAR_URL
from weather.utils.globals import SETTINGS_STUBS_METEAR_START_DATE
from weather.models import set_metear_start_date

SOCAT = "socat"
TIMEVORTEX_LOG_FILE = "/tmp/timevortex/timevortex.log"
DICT_JSON_REQUEST_HEADER = {'Content-type': 'application/json', 'Accept': '*/*'}
STUBS_COMMAND = "python manage.py runserver 0.0.0.0:8000"
KEY_LABEL = "label"
KEY_SITE_TYPE = "site_type"
WITH_STUBS = "with_stubs"


def reset_testing_environment():
    data_folder = getattr(settings, SETTINGS_FILE_STORAGE_FOLDER, SETTINGS_DEFAULT_FILE_STORAGE_FOLDER)
    if exists(data_folder):
        shutil.rmtree(data_folder)
    setattr(settings, SETTINGS_METEAR_URL, SETTINGS_STUBS_METEAR_URL)
    set_metear_start_date(SETTINGS_STUBS_METEAR_START_DATE)


def assert_equal(element1, element2):
    try:
        assert element1 in element2, "%s should equal to %s" % (element1, element2)
    except TypeError:
        assert element1 == element2, "%s should equal to %s" % (element1, element2)


def assert_gte(element1, element2):
    assert element1 >= element2, "%s should be gte to %s" % (element1, element2)


def assert_lte(element1, element2):
    assert element1 <= element2, "%s should be lte to %s" % (element1, element2)


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
        assert_equal(c[word], expected_occurency)
