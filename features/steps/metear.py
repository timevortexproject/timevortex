#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""Functionnal test for METEAR"""

from io import StringIO
from datetime import datetime, timedelta
from django.conf import settings
from behave import given  # pylint: disable=I0011,E0611
from timevortex.models import get_site_by_slug, get_site_variables
from timevortex.utils.filestorage import FILE_STORAGE_SPACE
from weather.utils.globals import SETTINGS_METEAR_URL, SETTINGS_STUBS_NEW_METEAR_URL
from weather.management.commands.retrieve_metear_data import Command as MetearCommand
from features.steps.test_globals import assertEqual, counter_from_log


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


@given("I add a bad metear url in settings")
def define_wrong_metear_url(context):  # pylint: disable=I0011,W0613
    """Define wrong metear URL
    """
    setattr(settings, SETTINGS_METEAR_URL, SETTINGS_BAD_METEAR_URL)


@given("I configure metear web service to generate bad content")
def define_bad_content_metear_ws(context):  # pylint: disable=I0011,W0613
    """Define bad content METEAR Webservice
    """
    setattr(settings, SETTINGS_METEAR_URL, SETTINGS_BAD_CONTENT_METEAR_URL)


@given("new data are available")
def new_data_available(context):  # pylint: disable=I0011,W0613
    """New data available
    """
    setattr(settings, SETTINGS_METEAR_URL, SETTINGS_STUBS_NEW_METEAR_URL)


@given("I run for the first time the metear script")
def run_metear_script_populate(context):  # pylint: disable=I0011,W0613
    """Run METEAR script populate
    """
    out = StringIO()
    command = MetearCommand()
    command.out = out
    command.handle()


def transform_metear_array2dict(array):  # pylint: disable=I0011,W0613
    """Transform METEAR array into dict
    """
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


def launch_metear_command(out):
    """Launch METEAR command
    """
    command = MetearCommand()
    command.out = out
    command.handle()


def verify_metear_data_update(site_id, data_type):
    """Verify METEAR data update
    """
    start_array_index = 0
    end_array_index = -2
    site = get_site_by_slug(slug=site_id)
    fixtures = DICT_METEAR_FAKE_DATA
    if data_type in "new":
        counter_from_log("GET", 1, TIMEVORTEX_WEATHER_LOG_FILE, -3)
        counter_from_log("GET", 0, TIMEVORTEX_WEATHER_LOG_FILE, -4)
        fixtures = DICT_METEAR_FAKE_NEWS_DATA
    variables = get_site_variables(site=site)
    expected_variables_len = len(fixtures[start_array_index][KEY_METEAR_FAKE_DATA_ELEMENTS]) - 1
    expected_start_date = "%s+00:00" % fixtures[start_array_index][KEY_METEAR_FAKE_DATA_DATE]
    expected_end_date = "%s+00:00" % fixtures[end_array_index][KEY_METEAR_FAKE_DATA_DATE]
    expected_start_value = transform_metear_array2dict(
        fixtures[start_array_index][KEY_METEAR_FAKE_DATA_ELEMENTS])
    expected_end_value = transform_metear_array2dict(
        fixtures[end_array_index][KEY_METEAR_FAKE_DATA_ELEMENTS])
    assertEqual(len(variables), expected_variables_len)
    for variable in variables:
        assertEqual(variable.start_date.isoformat(" "), expected_start_date)
        assertEqual(variable.end_date.isoformat(" "), expected_end_date)
        assertEqual(variable.start_value, expected_start_value[variable.slug])
        assertEqual(variable.end_value, expected_end_value[variable.slug])


def verify_metear_tsv_update(site_id, data_type):
    """Verify METEAR TSV update
    """
    fixtures = DICT_METEAR_FAKE_DATA
    if data_type in "new":
        fixtures = DICT_METEAR_FAKE_NEWS_DATA
    fixtures_data = {}
    folder_data = {}
    for fix in fixtures:
        if fix[KEY_METEAR_FAKE_DATA_STATUS] == KEY_METEAR_FAKE_DATA_OK:
            variables = transform_metear_array2dict(fix[KEY_METEAR_FAKE_DATA_ELEMENTS])
            for key in variables:
                if key not in fixtures_data:
                    fixtures_data[key] = {}
                    folder_data[key] = FILE_STORAGE_SPACE.get_series(site_id, key)
                fixtures_data[key][fix[KEY_METEAR_FAKE_DATA_DATE]] = variables[key]

    for variable in fixtures_data:
        for date in fixtures_data[variable]:
            iso_date = "%s+00:00" % date.replace(" ", "T")
            assertEqual(fixtures_data[variable][date], folder_data[variable][iso_date])
