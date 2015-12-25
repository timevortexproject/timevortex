#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""Commands utils file"""

import sys
import requests
from django.core.management.base import BaseCommand
from timevortex.utils.globals import LOGGER


class HTMLCrawlerCommand(BaseCommand):
    """Class that let us define a generic workflow to retrieve
    html content over internet.
    """
    out = sys.stdout
    url = ""
    html = ""
    row = ""
    transformed_row = ""
    message = ""
    variable_id = ""
    multi_rows = False
    multi_variables_per_row = False
    variables = []
    error_bad_url = "Bad URL."
    error_problem_ws = "Problem Web Service."

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
            response.raise_for_status()
            self.html = response.content.decode("utf-8")
        except requests.exceptions.ConnectionError:
            self.html = None
            self.out.write("%s\n" % self.error_bad_url)
            LOGGER.error(self.error_bad_url)
            return
        except requests.exceptions.HTTPError:
            self.html = None
            self.out.write("%s\n" % self.error_problem_ws)
            LOGGER.error(self.error_problem_ws)
            return

    def send_message(self):
        """Send message through RBMQ
        """
        self.out.write("%s\n" % self.message)
        LOGGER.error(self.message)

    def prepare_message(self):
        """Method that prepare message in order to send it through
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
        if self.multi_rows:
            for row in self.html:
                self.row = row
                if self.multi_variables_per_row:
                    self.prepare_row()
                    if self.transformed_row is not None:
                        for variable_id in self.variables:
                            self.variable_id = variable_id
                            self.prepare_message()
                            if self.message is not None:
                                self.send_message()
