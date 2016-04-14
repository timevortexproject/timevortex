#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-
# pylint: disable=R0904

"""
    Test file for FileStorage class.
"""

from datetime import date, datetime
from django.test import TestCase
from timevortex.utils.filestorage import FILE_STORAGE_SPACE
from timevortex.utils.globals import KEY_ERROR, KEY_SITE_ID, KEY_VARIABLE_ID, KEY_VALUE, KEY_DATE
from timevortex.utils.globals import KEY_DST_TIMEZONE, KEY_NON_DST_TIMEZONE
from timevortex.management.commands.daily_report import get_sites_information, KEY_REPORT_NAME
from timevortex.management.commands.daily_report import KEY_REPORT_ERROR_NUMBERS, KEY_REPORT_SERIES_NUMBERS
from timevortex.tests.utils import clean_folder

from features.steps.test_utils import TEST_CC_SITE_ID


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
EXPECTED_SITES_INFO = {
    TEST_CC_SITE_ID: {
        KEY_REPORT_ERROR_NUMBERS: ERROR_NUMBER,
        KEY_REPORT_SERIES_NUMBERS: {
            TEST_VARIABLE: {"value": 12},
            "not_a_test": {"value": 23},
            "test_2": {"value": 5}}
    },
    "system": {
        KEY_REPORT_ERROR_NUMBERS: 1,
        KEY_REPORT_SERIES_NUMBERS: {}
    }
}


class TestDailyReport(TestCase):
    """
        All test case for daily_report command.

        Tests:

        * Create a series and errors and send email
    """

    def setUp(self):
        clean_folder()

    # def tearDown(self):
    #     clean_folder()

    def test_sending_email(self):
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

        error = {
            KEY_SITE_ID: TEST_CC_SITE_ID,
            KEY_VARIABLE_ID: KEY_ERROR,
            KEY_DATE: datetime.utcnow().isoformat(),
            KEY_DST_TIMEZONE: "CET",
            KEY_NON_DST_TIMEZONE: "CEST"
        }

        error_2 = {
            KEY_VALUE: "System collapse",
            KEY_SITE_ID: "system",
            KEY_VARIABLE_ID: KEY_ERROR,
            KEY_DATE: datetime.utcnow().isoformat(),
            KEY_DST_TIMEZONE: "CET",
            KEY_NON_DST_TIMEZONE: "CEST"
        }

        FILE_STORAGE_SPACE.insert_series(trap_series)
        FILE_STORAGE_SPACE.insert_error(error_2)

        for variable in VARIABLES:
            series[KEY_VARIABLE_ID] = variable
            for i in range(VARIABLES[variable][KEY_VALUE]):
                series[KEY_VALUE] = i
                FILE_STORAGE_SPACE.insert_series(series)

        for i in range(ERROR_NUMBER):
            error[KEY_VALUE] = i
            FILE_STORAGE_SPACE.insert_error(error)

        day_date = datetime.now().strftime("%Y-%m-%d")
        result = get_sites_information(day_date)
        print(result)
        print(day_date)

        self.assertEqual(len(result), len(EXPECTED_SITES_INFO))

        new_result = {}

        for index in range(len(result)):
            new_result[result[index][KEY_REPORT_NAME]] = {
                KEY_REPORT_ERROR_NUMBERS: result[index][KEY_REPORT_ERROR_NUMBERS],
                KEY_REPORT_SERIES_NUMBERS:result[index][KEY_REPORT_SERIES_NUMBERS]
            }

        print(new_result)

        for site in new_result:
            self.assertIn(site, EXPECTED_SITES_INFO)
            self.assertEqual(
                new_result[site][KEY_REPORT_ERROR_NUMBERS], EXPECTED_SITES_INFO[site][KEY_REPORT_ERROR_NUMBERS])
            self.assertEqual(
                new_result[site][KEY_REPORT_SERIES_NUMBERS], EXPECTED_SITES_INFO[site][KEY_REPORT_SERIES_NUMBERS])