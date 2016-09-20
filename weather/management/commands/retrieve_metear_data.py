#!/usr/bin/python3
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""METEAR command"""

import sys
import logging
from datetime import timedelta
import dateutil.parser
import pytz
from django.conf import settings
from django.utils import timezone
from timevortex.utils.commands import HTMLCrawlerCommand, AbstractCommand
from timevortex.utils.globals import timeseries_json, KEY_DATE
from timevortex.models import Site, get_site_by_slug_and_type, get_sites_by_type, update_or_create_variable
from timevortex.models import get_variable_by_slug
from weather.utils.globals import ERROR_METEAR, KEY_METEAR_NO_SITE_ID, SETTINGS_METEAR_URL, SETTINGS_DEFAULT_METEAR_URL
from weather.utils.globals import KEY_METEAR_BAD_URL, KEY_METEAR_PROBLEM_WS, KEY_METEAR_BAD_CONTENT
from weather.utils.globals import SETTINGS_METEAR_START_DATE, SETTINGS_DEFAULT_METEAR_START_DATE

LOGGER = logging.getLogger("weather")
SLUG_METEAR_TEMPERATURE_CELSIUS = "metear_temperature_celsius"
ARRAY_VARIABLE_ID = [
    SLUG_METEAR_TEMPERATURE_CELSIUS,
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
    "metear_wind_direction_degrees",
]
TODAY = timezone.now()


class MyMETEARCrawler(HTMLCrawlerCommand):  # pylint: disable=I0011,R0902
    """Command class
    """

    help = 'Retrieve metear data from weather underground website'
    reverse = False
    multi_rows = True
    multi_variables_per_row = True
    error_bad_url = ERROR_METEAR[KEY_METEAR_BAD_URL]
    error_problem_ws = ERROR_METEAR[KEY_METEAR_PROBLEM_WS]
    error_bad_content = ERROR_METEAR[KEY_METEAR_BAD_CONTENT]
    variables = ARRAY_VARIABLE_ID

    def url_generator(self, *args, **options):
        """Generate METEAR url according to site_id and date
        """
        from_date = "%s/%s/%s" % (TODAY.year, TODAY.month, TODAY.day)
        if "site_id" not in options:
            self.out.write("%s\n" % ERROR_METEAR[KEY_METEAR_NO_SITE_ID])
            self.logger.error(ERROR_METEAR[KEY_METEAR_NO_SITE_ID])
            return
        if "from_date" in options:
            from_date = options["from_date"].strftime("%Y/%m/%d")
        self.site_id = options["site_id"]
        metear_url = getattr(settings, SETTINGS_METEAR_URL, SETTINGS_DEFAULT_METEAR_URL)
        self.url = metear_url % (self.site_id, from_date)

    def clean_data(self):
        """Clean data receive form METEAR API, remove <br/> and \n
        """
        self.html = self.html.replace("<br/>", "").replace("<br />", "").split("\n")[2:]
        if self.reverse:
            self.html = self.remove_html_duplication()
            self.html = self.html[::-1]

    def remove_html_duplication(self):
        """Remove duplicate line into METAER data API
        """
        elements = []
        for item in self.html:
            key = item.split(",")[0]
            if key not in elements:
                elements.append(key)
            else:
                self.html.remove(item)
        return self.html

    def prepare_row(self):
        """Prepare HTML row to contain clear value
        """
        self.transformed_row = None
        transformed_row = {}
        self.row = self.row.split(",")[1:]
        if len(self.row) > len(self.variables):
            # self.logger.debug("Row")
            # self.logger.debug(self.row)
            try:
                transformed_row[KEY_DATE] = dateutil.parser.parse(self.row[-1]).replace(tzinfo=pytz.UTC)
                for i in range(len(self.variables)):
                    transformed_row[self.variables[i]] = self.row[i]
                self.transformed_row = transformed_row
            except ValueError:
                pass

    def prepare_timeseries(self):
        """Transform row into timeseries
        """
        self.timeseries = None
        value = self.transformed_row[self.variable_id]
        row_date = self.transformed_row[KEY_DATE]
        site = get_site_by_slug_and_type(slug=self.site_id, site_type=Site.METEAR_TYPE)
        variable = update_or_create_variable(site=site, slug=self.variable_id, date=row_date, value=value)
        if variable is not None:
            self.timeseries = timeseries_json(self.site_id, self.variable_id, value, row_date.isoformat())


class Command(AbstractCommand):
    """Command class
    """
    help = "Retrieve METEAR data from weatherunderground website"
    out = sys.stdout
    name = "METEAR crawler"
    logger = LOGGER

    def launch_crawler(self, metear_sites):
        """Launch METEAR crawler
        """
        crawler = MyMETEARCrawler()
        crawler.set_logger(LOGGER)
        crawler.out = self.out
        crawler.reverse = False
        settings_start_date = getattr(settings, SETTINGS_METEAR_START_DATE, SETTINGS_DEFAULT_METEAR_START_DATE)
        bound_start_date = dateutil.parser.parse(settings_start_date).replace(tzinfo=pytz.UTC)
        bound_end_date = TODAY
        for site in metear_sites:
            variable_start_date = bound_end_date
            variable_end_date = bound_end_date
            variable = get_variable_by_slug(site=site, slug=SLUG_METEAR_TEMPERATURE_CELSIUS)
            if variable is not None:
                variable_start_date = variable.start_date
                variable_end_date = variable.end_date
            ending_date = bound_end_date.date()
            while variable_end_date.date() <= ending_date:
                crawler.handle(site_id=site.slug, from_date=variable_end_date)
                variable_end_date += timedelta(days=1)
            crawler.reverse = True
            ending_date = bound_start_date.date()
            while variable_start_date.date() >= ending_date:
                crawler.handle(site_id=site.slug, from_date=variable_start_date)
                variable_start_date += timedelta(days=-1)

    def run(self, *args, **options):
        metear_sites = get_sites_by_type(site_type=Site.METEAR_TYPE)
        if len(metear_sites) > 0:
            self.launch_crawler(metear_sites)
        else:
            self.send_error(ERROR_METEAR[KEY_METEAR_NO_SITE_ID])
