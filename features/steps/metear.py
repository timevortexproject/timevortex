#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""Functionnal test for METEAR"""

import os
import json
import shlex
import subprocess
from time import sleep
from io import StringIO
from django.conf import settings
from behave import given, then
from features.steps.test_utils import stubs_change_api_configuration
from features.steps.test_utils import TEST_METEAR_SITE_ID_2, DICT_METEAR_FAKE_NEWS_DATA
from features.steps.test_utils import TEST_METEAR_LABEL_2, DICT_METEAR_FAKE_DATA, KEY_METEAR_FAKE_DATA_ELEMENTS
from features.steps.test_utils import TEST_METEAR_LABEL, SETTINGS_BAD_METEAR_URL, SETTINGS_BAD_CONTENT_METEAR_URL
from features.steps.test_utils import KEY_METEAR_FAKE_DATA_DATE, transform_metear_array_into_dict, TEST_METEAR_SITE_ID
from features.steps.test_utils import counter_from_log, error_in_list, verify_json_message, KEY_METEAR_FAKE_DATA_OK
from features.steps.test_utils import KEY_METEAR_FAKE_DATA_STATUS, assertEqual, reset_testing_environment
from features.steps.test_utils import TIMEVORTEX_WEATHER_LOG_FILE
from timevortex.models import Site, Variable
from timevortex.utils.globals import LOGGER
from weather.utils.globals import SETTINGS_METEAR_URL, SETTINGS_STUBS_NEW_METEAR_URL
from weather.management.commands.retrieve_metear_data import Command
from stubs.utils.globals import KEY_STUBS_OPEN_METEAR_API
from timevortex.utils.globals import KEY_VALUE, SYSTEM_SITE_ID, KEY_SITE_ID, KEY_VARIABLE_ID
from timevortex.utils.filestorage import FILE_STORAGE_SPACE

STUBS_COMMAND = "python manage.py runserver 0.0.0.0:8000"


@given("I created a testing Site '{site_id}'")
def create_testing_site(context, site_id):
    LOGGER.debug("Start creation site")
    reset_testing_environment()
    if site_id in TEST_METEAR_SITE_ID:
        Site.objects.create(slug=TEST_METEAR_SITE_ID, label=TEST_METEAR_LABEL, site_type=Site.METEAR_TYPE)
    elif site_id in TEST_METEAR_SITE_ID_2:
        Site.objects.create(slug=TEST_METEAR_SITE_ID_2, label=TEST_METEAR_LABEL_2, site_type=Site.METEAR_TYPE)
    context.site_id = site_id
    commands = STUBS_COMMAND
    context.stubs = subprocess.Popen(shlex.split(commands), stdout=subprocess.PIPE, preexec_fn=os.setsid)
    sleep(1)
    stubs_change_api_configuration({KEY_STUBS_OPEN_METEAR_API: True})


@given("I add a bad metear url in settings")
def define_wrong_metear_url(context):
    setattr(settings, SETTINGS_METEAR_URL, SETTINGS_BAD_METEAR_URL)


@given("I shutdown the metear web service")
def shutdown_metear_ws(context):
    stubs_change_api_configuration({KEY_STUBS_OPEN_METEAR_API: False})


@given("I configure metear web service to generate bad content")
def define_bad_content_metear_ws(context):
    setattr(settings, SETTINGS_METEAR_URL, SETTINGS_BAD_CONTENT_METEAR_URL)


@given("new data are available")
def new_data_available(context):
    setattr(settings, SETTINGS_METEAR_URL, SETTINGS_STUBS_NEW_METEAR_URL)


@given("I run for the first time the metear script")
def run_metear_script_populate(context):
    out = StringIO()
    command = Command()
    command.out = out
    command.handle()


@then("I should see '{data_type}' data update in DB for '{site_id}'")
def verify_data_update_db(context, data_type, site_id):
    start_array_index = 0
    end_array_index = -2
    if site_id in TEST_METEAR_SITE_ID:
        site = Site.objects.filter(slug=TEST_METEAR_SITE_ID, site_type=Site.METEAR_TYPE)
    elif site_id in TEST_METEAR_SITE_ID_2:
        site = Site.objects.filter(slug=TEST_METEAR_SITE_ID_2, site_type=Site.METEAR_TYPE)
    fixtures = DICT_METEAR_FAKE_DATA
    if data_type in "new":
        counter_from_log("GET", 1, TIMEVORTEX_WEATHER_LOG_FILE, -3)
        counter_from_log("GET", 0, TIMEVORTEX_WEATHER_LOG_FILE, -4)
        fixtures = DICT_METEAR_FAKE_NEWS_DATA
    variables = Variable.objects.filter(site=site)
    expected_variables_len = len(fixtures[start_array_index][KEY_METEAR_FAKE_DATA_ELEMENTS]) - 1
    expected_start_date = "%s+00:00" % fixtures[start_array_index][KEY_METEAR_FAKE_DATA_DATE]
    expected_end_date = "%s+00:00" % fixtures[end_array_index][KEY_METEAR_FAKE_DATA_DATE]
    expected_start_value = transform_metear_array_into_dict(
        fixtures[start_array_index][KEY_METEAR_FAKE_DATA_ELEMENTS])
    expected_end_value = transform_metear_array_into_dict(
        fixtures[end_array_index][KEY_METEAR_FAKE_DATA_ELEMENTS])
    assert len(variables) == expected_variables_len, "%s should equal to %s" % (len(variables), expected_variables_len)
    for variable in variables:
        assert variable.start_date.isoformat(" ") in expected_start_date, "variable.start_d: %s should equal to %s" % (
            variable.start_date, expected_start_date)
        assert variable.end_date.isoformat(" ") in expected_end_date, "variable.end_date: %s should equal to %s" % (
            variable.end_date, expected_end_date)
        assert variable.start_value == expected_start_value[variable.slug], "var.start_val: %s should equal to %s" % (
            variable.start_value, expected_start_value[variable.slug])
        assert variable.end_value == expected_end_value[variable.slug], "var.end_val: %s should equal to %s" % (
            variable.end_value, expected_end_value[variable.slug])


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
    assert error in last_error[KEY_VALUE], "%s should equal to %s" % (error, last_error[KEY_VALUE])


@then("I should see '{data_type}' data update in TSV file for '{site_id}'")
def verify_data_update_tsv_file(context, data_type, site_id):
    try:
        expected_message = json.loads(context.specific_error)
        site_id = expected_message[KEY_SITE_ID]
        variable_id = expected_message[KEY_VARIABLE_ID]
        last_series = FILE_STORAGE_SPACE.get_last_series(site_id, variable_id)
        verify_json_message(last_series, expected_message)
        return
    except AttributeError:
        fixtures = DICT_METEAR_FAKE_DATA
        if data_type in "new":
            fixtures = DICT_METEAR_FAKE_NEWS_DATA
        fixtures_data = {}
        folder_data = {}
        for fix in fixtures:
            if fix[KEY_METEAR_FAKE_DATA_STATUS] == KEY_METEAR_FAKE_DATA_OK:
                variables = transform_metear_array_into_dict(fix[KEY_METEAR_FAKE_DATA_ELEMENTS])
                for key in variables:
                    if key not in fixtures_data:
                        fixtures_data[key] = {}
                        folder_data[key] = FILE_STORAGE_SPACE.get_series(site_id, key)
                    fixtures_data[key][fix[KEY_METEAR_FAKE_DATA_DATE]] = variables[key]

        for variable in fixtures_data:
            for date in fixtures_data[variable]:
                iso_date = "%s+00:00" % date.replace(" ", "T")
                assertEqual(fixtures_data[variable][date], folder_data[variable][iso_date])
