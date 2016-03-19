#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-
# pylint: disable=R0904

"""
    Test file for FileStorage class.
"""

import shutil
from os.path import exists
from datetime import date, datetime
from django.test import TestCase
from django.conf import settings
from timevortex.utils.filestorage import FILE_STORAGE_SPACE, SETTINGS_FILE_STORAGE_FOLDER
from timevortex.utils.filestorage import SETTINGS_DEFAULT_FILE_STORAGE_FOLDER
from timevortex.utils.globals import LOGGER, KEY_ERROR, KEY_SITE_ID, KEY_VARIABLE_ID, KEY_VALUE, KEY_DATE
from timevortex.utils.globals import KEY_DST_TIMEZONE, KEY_NON_DST_TIMEZONE
from features.steps.test_utils import TEST_CC_SITE_ID

STORAGE_SPACE = getattr(settings, SETTINGS_FILE_STORAGE_FOLDER, SETTINGS_DEFAULT_FILE_STORAGE_FOLDER)
ERROR_NUMBER = 5
TEST_VARIABLE = "test"
VARIABLES = {
    TEST_VARIABLE: {
        "value": 12
    },
    "not_a_test": {
        "value": 23
    },
    "test_2": {
        "value": 5
    }
}
FAKE_DATE = "2012-05-08"
SECOND_FAKE_DATE = "2014-03-22"


FOLDER_PATH = "%s/%s" % (STORAGE_SPACE, TEST_CC_SITE_ID)
if exists(FOLDER_PATH):
    shutil.rmtree(FOLDER_PATH)


class TestFileStorage(TestCase):
    """
        All test case for messaging method.

        Tests:

        * Create a series and read it
        * Create an error and read it
    """

    def test_series_creation(self):
        """
            Test series creation.
        """
        series = {
            KEY_SITE_ID: TEST_CC_SITE_ID,
            KEY_DATE: datetime.utcnow().isoformat("T"),
            KEY_DST_TIMEZONE: "CET",
            KEY_NON_DST_TIMEZONE: "CEST"
        }

        trap_series = {
            KEY_VARIABLE_ID: TEST_VARIABLE,
            KEY_VALUE: "12",
            KEY_SITE_ID: TEST_CC_SITE_ID,
            KEY_DATE: "2014-03-22T00:00:00.000000",
            KEY_DST_TIMEZONE: "CET",
            KEY_NON_DST_TIMEZONE: "CEST"
        }

        FILE_STORAGE_SPACE.insert_series(trap_series)

        for variable in VARIABLES:
            series[KEY_VARIABLE_ID] = variable
            for i in range(VARIABLES[variable][KEY_VALUE]):
                series[KEY_VALUE] = i
                FILE_STORAGE_SPACE.insert_series(series)

        for variable in VARIABLES:
            result = FILE_STORAGE_SPACE.get_last_series(TEST_CC_SITE_ID, variable)
            series[KEY_VALUE] = VARIABLES[variable][KEY_VALUE] - 1
            series[KEY_VARIABLE_ID] = variable
            self.assertEqual(series[KEY_VALUE], int(result[KEY_VALUE]))
            self.assertEqual(series[KEY_SITE_ID], result[KEY_SITE_ID])
            self.assertEqual(series[KEY_VARIABLE_ID], result[KEY_VARIABLE_ID])
            self.assertEqual(series[KEY_DST_TIMEZONE], result[KEY_DST_TIMEZONE])
            self.assertEqual(
                series[KEY_NON_DST_TIMEZONE], result[KEY_NON_DST_TIMEZONE])
            self.assertEqual(series[KEY_DATE], result[KEY_DATE])

        today = date.today().isoformat()
        series_number = FILE_STORAGE_SPACE.get_number_of_series(
            TEST_CC_SITE_ID, today)
        LOGGER.error(series_number)
        self.assertEqual(len(series_number), len(VARIABLES))
        for variable in VARIABLES:
            self.assertEqual(variable in series_number, True)
            self.assertEqual(
                series_number[variable][KEY_VALUE], VARIABLES[variable][KEY_VALUE])

        series_number = FILE_STORAGE_SPACE.get_number_of_series(
            TEST_CC_SITE_ID, FAKE_DATE)
        self.assertEqual(len(series_number), 0)

        series_number = FILE_STORAGE_SPACE.get_number_of_series(
            TEST_CC_SITE_ID, SECOND_FAKE_DATE)
        self.assertEqual(len(series_number), 1)
        variable = TEST_VARIABLE
        self.assertEqual(variable in series_number, True)
        self.assertEqual(
            series_number[variable][KEY_VALUE], 1)

    def test_error_creation(self):
        """
            Test error creation.
        """
        error = {
            KEY_SITE_ID: TEST_CC_SITE_ID,
            KEY_VARIABLE_ID: KEY_ERROR,
            KEY_DATE: datetime.utcnow().isoformat(),
            KEY_DST_TIMEZONE: "CET",
            KEY_NON_DST_TIMEZONE: "CEST"
        }

        for i in range(ERROR_NUMBER):
            error[KEY_VALUE] = i
            FILE_STORAGE_SPACE.insert_error(error)

        result = FILE_STORAGE_SPACE.get_last_error(TEST_CC_SITE_ID)
        self.assertEqual(error[KEY_VALUE], int(result[KEY_VALUE]))
        self.assertEqual(error[KEY_SITE_ID], result[KEY_SITE_ID])
        self.assertEqual(error[KEY_VARIABLE_ID], result[KEY_VARIABLE_ID])
        self.assertEqual(error[KEY_DST_TIMEZONE], result[KEY_DST_TIMEZONE])
        self.assertEqual(error[KEY_NON_DST_TIMEZONE], result[KEY_NON_DST_TIMEZONE])
        self.assertEqual(error[KEY_DATE], result[KEY_DATE])

        today = date.today().isoformat()
        result = FILE_STORAGE_SPACE.get_number_of_error(TEST_CC_SITE_ID, today)
        LOGGER.error(result)
        self.assertEqual(result, ERROR_NUMBER)

        result = FILE_STORAGE_SPACE.get_number_of_error(TEST_CC_SITE_ID, FAKE_DATE)
        self.assertEqual(result, 0)
