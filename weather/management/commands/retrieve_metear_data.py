#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""Metear command"""

import sys
from time import tzname
from datetime import date
from django.conf import settings
from django.core.management.base import BaseCommand
from timevortex.utils.commands import HTMLCrawlerCommand
from timevortex.utils.globals import LOGGER, KEY_SITE_ID, KEY_VARIABLE_ID, KEY_VALUE
from timevortex.utils.globals import KEY_DATE, KEY_DST_TIMEZONE, KEY_NON_DST_TIMEZONE
from weather.utils.globals import ERROR_METEAR, KEY_METEAR_NO_SITE_ID, SETTINGS_METEAR_URL, SETTINGS_DEFAULT_METEAR_URL
from weather.utils.globals import KEY_METEAR_BAD_URL, KEY_METEAR_PROBLEM_WS
from timevortex.models import Sites

AIRPORT_ID = "LFMN"
SITE_ID = "liogen_city"
ARRAY_VARIABLE_ID = [
    "metear_temperature_celsius",
    "metear_dew_point_celsius",
    "metear_humidity_percentage",
    "metear_sea_level_pressure_hpa",
    "metear_visibility_km",
    "metear_wind_direction",
    "metear_wind_speed_kmh",
    "metear_gust_speed_kmh",
    "metear_precipitation_mm",
    "metear_events",
    "metear_conditions",
    "metear_wind_direction_degrees"
]


class MyMETEARCrawler(HTMLCrawlerCommand):
    """Command class
    """

    help = 'Retrieve metear data from weather underground website'

    multi_rows = True
    multi_variables_per_row = True
    error_bad_url = ERROR_METEAR[KEY_METEAR_BAD_URL]
    error_problem_ws = ERROR_METEAR[KEY_METEAR_PROBLEM_WS]
    variables = ARRAY_VARIABLE_ID

    def url_generator(self, *args, **options):
        metear_url = getattr(settings, SETTINGS_METEAR_URL, SETTINGS_DEFAULT_METEAR_URL)
        today = date.today()
        today_string = "%s/%s/%s" % (today.year, today.month, today.day)
        self.url = metear_url % (AIRPORT_ID, today_string)

    def clean_data(self):
        self.html = self.html.replace("<br/>", "").replace("<br />", "").split("\n")[2:]

    def prepare_row(self):
        self.transformed_row = None
        transformed_row = {}
        self.row = self.row.split(",")[1:]
        if len(self.row) > len(self.variables):
            transformed_row[KEY_DATE] = self.row[-1]
            for i in range(len(self.variables)):
                transformed_row[self.variables[i]] = self.row[i]
            self.transformed_row = transformed_row

    def prepare_message(self):
        site_id = SITE_ID
        value = self.transformed_row[self.variable_id]
        row_date = self.transformed_row[KEY_DATE]
        self.message = {
            KEY_SITE_ID: site_id,
            KEY_VARIABLE_ID: self.variable_id,
            KEY_VALUE: value,
            KEY_DATE: row_date,
            KEY_DST_TIMEZONE: tzname[1],
            KEY_NON_DST_TIMEZONE: tzname[0]
        }


class Command(BaseCommand):
    """Command class
    """
    help = "Retireve METEAR data from weatherunderground website"
    out = sys.stdout

    def handle(self, *args, **options):
        try:
            metear_sites = Sites.objects.filter(site_type=Sites.METEAR_TYPE)
        except Sites.DoesNotExist:
            metear_sites = []
        LOGGER.debug(metear_sites)
        if len(metear_sites) == 0:
            self.out.write("%s\n" % ERROR_METEAR[KEY_METEAR_NO_SITE_ID])
            LOGGER.error(ERROR_METEAR[KEY_METEAR_NO_SITE_ID])
            return
        crawler = MyMETEARCrawler()
        crawler.out = self.out
        crawler.handle()
