#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""Commands utils file"""

import sys
import json
import requests
from time import tzname
from django.core.management.base import BaseCommand
from django.utils import timezone
from timevortex.utils.globals import ERROR_TIMESERIES_NOT_DEFINED
from timevortex.utils.signals import SIGNAL_TIMESERIES
from timevortex.utils.globals import KEY_SITE_ID, KEY_VARIABLE_ID, KEY_VALUE, KEY_DATE, KEY_DST_TIMEZONE
from timevortex.utils.globals import KEY_NON_DST_TIMEZONE, KEY_ERROR


class AbstractCommand(BaseCommand):
    """Abstact class that provide helpful method for django command
    """

    def set_logger(self, logger):
        self.logger = logger

    def send_timeseries(self):
        """Send pub/sub timeseries timeseries
        """
        try:
            # LOGGER.debug("send timeseries")
            # LOGGER.debug(self.timeseries)
            timeseries = json.dumps(self.timeseries)
            SIGNAL_TIMESERIES.send(sender=self.__class__, timeseries=timeseries)
        except AttributeError:
            self.logger.error(ERROR_TIMESERIES_NOT_DEFINED)

    def send_error(self, error):
        try:
            error_message = json.dumps({
                KEY_SITE_ID: self.site_id,
                KEY_VARIABLE_ID: KEY_ERROR,
                KEY_VALUE: error,
                KEY_DATE: timezone.now().isoformat(),
                KEY_DST_TIMEZONE: tzname[1],
                KEY_NON_DST_TIMEZONE: tzname[0]
            })
            SIGNAL_TIMESERIES.send(sender=self.__class__, timeseries=error_message)
        except AttributeError:
            pass
        self.out.write("%s\n" % error)
        self.logger.error(error)

    def run(self, *args, **options):
        pass

    def handle(self, *args, **options):
        self.logger.info("Command %s started", self.name)
        self.run(*args, **options)
        self.logger.info("Command %s stopped", self.name)


class HTMLCrawlerCommand(AbstractCommand):
    """Class that let us define a generic workflow to retrieve
    html content over internet.
    """
    site_id = ""
    out = sys.stdout
    url = ""
    html = ""
    row = ""
    transformed_row = ""
    timeseries = ""
    variable_id = ""
    multi_rows = False
    multi_variables_per_row = False
    variables = []
    error_bad_url = "Problem bad URL."
    error_problem_ws = "Problem Web Service."
    error_bad_content = "Problem bad content."

    def url_generator(self, *args, **options):
        """Generate URL to call the webservice
        """
        pass

    def clean_data(self):
        """Clean HTML data receive in order to parse them
        """
        pass

    def prepare_row(self):
        """Prepare row to be parsed
        """
        pass

    def open_html_file(self):
        """Call the HTML page and retrieve the result. Return None if there is a HTTPError
        """
        try:
            response = requests.get(self.url)
            self.logger.info("GET %s" % self.url)
            response.raise_for_status()
            self.html = response.content.decode("utf-8")
        except requests.exceptions.ConnectionError:
            self.html = None
            self.send_error(self.error_bad_url)
        except requests.exceptions.HTTPError:
            self.html = None
            self.send_error(self.error_problem_ws)
            return

    def prepare_timeseries(self):
        """Method that prepare timeseries in order to send it through
        RBMQ.
        """
        if self.variable_id in self.row:
            return self.row
        return None

    def handle(self, *args, **options):
        self.url_generator(self, *args, **options)
        self.open_html_file()
        if self.html is None:
            return
        self.clean_data()
        if len(self.html) == 0:
            self.send_error(self.error_bad_content)
            return
        if self.multi_rows:
            for row in self.html:
                self.row = row
                if self.multi_variables_per_row:
                    self.prepare_row()
                    if self.transformed_row is not None:
                        for variable_id in self.variables:
                            self.variable_id = variable_id
                            self.prepare_timeseries()
                            if self.timeseries is not None and self.timeseries != "":
                                self.send_timeseries()
