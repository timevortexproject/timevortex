#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""METEAR command"""

import sys
import logging
from time import tzname
from datetime import timedelta
import dateutil.parser
import pytz
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from timevortex.utils.commands import HTMLCrawlerCommand, AbstractCommand
from timevortex.utils.globals import KEY_SITE_ID, KEY_VARIABLE_ID, KEY_VALUE
from timevortex.utils.globals import KEY_DATE, KEY_DST_TIMEZONE, KEY_NON_DST_TIMEZONE
from weather.utils.globals import ERROR_METEAR, KEY_METEAR_NO_SITE_ID, SETTINGS_METEAR_URL, SETTINGS_DEFAULT_METEAR_URL
from weather.utils.globals import KEY_METEAR_BAD_URL, KEY_METEAR_PROBLEM_WS, KEY_METEAR_BAD_CONTENT
from weather.utils.globals import SETTINGS_METEAR_START_DATE, SETTINGS_DEFAULT_METEAR_START_DATE
from timevortex.models import Site, Variable

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


class MyMETEARCrawler(HTMLCrawlerCommand):
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
        self.html = self.html.replace("<br/>", "").replace("<br />", "").split("\n")[2:]
        if self.reverse:
            self.html = self.remove_html_duplication()
            self.html = self.html[::-1]

    def remove_html_duplication(self):
        elements = []
        for item in self.html:
            key = item.split(",")[0]
            if key not in elements:
                elements.append(key)
            else:
                self.html.remove(item)
        return self.html

    def prepare_row(self):
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
        self.timeseries = None
        send = False
        value = self.transformed_row[self.variable_id]
        row_date = self.transformed_row[KEY_DATE]
        site = Site.objects.get(slug=self.site_id, site_type=Site.METEAR_TYPE)
        try:
            variable = Variable.objects.get(site=site, slug=self.variable_id)
            variable.update_value(row_date, value)
            variable.save()
            send = True
        except Variable.DoesNotExist:
            send = True
            Variable.objects.create(
                site=site,
                slug=self.variable_id,
                label=self.variable_id,
                start_date=row_date,
                start_value=value,
                end_date=row_date,
                end_value=value)
        except ValidationError:
            pass
        if send:
            self.timeseries = {
                KEY_SITE_ID: self.site_id,
                KEY_VARIABLE_ID: self.variable_id,
                KEY_VALUE: value,
                KEY_DATE: row_date.isoformat(),
                KEY_DST_TIMEZONE: tzname[1],
                KEY_NON_DST_TIMEZONE: tzname[0]
            }


class Command(AbstractCommand):
    """Command class
    """
    help = "Retireve METEAR data from weatherunderground website"
    out = sys.stdout
    name = "METEAR crawler"

    def handle(self, *args, **options):
        self.set_logger(LOGGER)
        self.logger.info("Command %s started", self.name)

        try:
            metear_sites = Site.objects.filter(site_type=Site.METEAR_TYPE)
        except Site.DoesNotExist:
            metear_sites = []
        if len(metear_sites) > 0:
            crawler = MyMETEARCrawler()
            crawler.set_logger(LOGGER)
            crawler.out = self.out
            settings_start_date = getattr(settings, SETTINGS_METEAR_START_DATE, SETTINGS_DEFAULT_METEAR_START_DATE)
            bound_start_date = dateutil.parser.parse(settings_start_date).replace(tzinfo=pytz.UTC)
            bound_end_date = TODAY
            for site in metear_sites:
                try:
                    variable = Variable.objects.get(site=site, slug=SLUG_METEAR_TEMPERATURE_CELSIUS)
                    variable_start_date = variable.start_date
                    variable_end_date = variable.end_date
                except Variable.DoesNotExist:
                    variable_start_date = bound_end_date
                    variable_end_date = bound_end_date
                # I have a set of value between start_date and end_date
                # If start_date is empty it get value of SETTINGS_METEAR_START_DATE in settings
                # If end_date is empty it get value of TODAY.date()
                # First I have to retrieve data between end_date and TODAY.date()
                # Then I will retrieve value between SETTINGS_METEAR_START_DATE and start_date
                while variable_end_date.date() <= bound_end_date.date():
                    crawler.reverse = False
                    crawler.handle(
                        site_id=site.slug,
                        from_date=variable_end_date)
                    variable_end_date += timedelta(days=1)
                while variable_start_date.date() >= bound_start_date.date():
                    crawler.reverse = True
                    crawler.handle(
                        site_id=site.slug,
                        from_date=variable_start_date)
                    variable_start_date += timedelta(days=-1)
        else:
            self.send_error(ERROR_METEAR[KEY_METEAR_NO_SITE_ID])
        self.logger.info("Command %s stopped", self.name)
