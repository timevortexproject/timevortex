#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""Currentcost command"""

import sys
import logging
from energy.utils.globals import KEY_ENERGY, MISSING_SITE_ID, ERROR_CURRENTCOST, MISSING_VARIABLE_ID
from timevortex.utils.commands import AbstractCommand

LOGGER = logging.getLogger(KEY_ENERGY)

def validate_argument(site_id):
    if site_id is None:
        return ERROR_CURRENTCOST[MISSING_SITE_ID]
    if variable_id is None:
        return ERROR_CURRENTCOST[MISSING_VARIABLE_ID]
    return None


class Command(AbstractCommand):
    """Command class
    """
    help = "Retrieve Currentcost data from Currentcost EnviR 128"
    out = sys.stdout
    name = "Currentcost connector"

    def handle(self, *args, **options):
        self.set_logger(LOGGER)
        self.logger.info("Command %s started", self.name)
        error_argument = validate_argument(None)
        if error_argument is None:
            print(12)
        self.send_error(error_argument)
        self.logger.info("Command %s stopped", self.name)
