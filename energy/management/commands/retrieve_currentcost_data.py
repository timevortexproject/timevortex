#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""Currentcost command"""

import sys
import serial
import logging
from time import sleep
from energy.utils.globals import KEY_ENERGY, ERROR_CURRENTCOST, ERROR_CC_NO_MESSAGE, ERROR_CC_BAD_PORT
from energy.utils.globals import TTY_CONNECTION_SUCCESS
from timevortex.utils.commands import AbstractCommand
# from timevortex.models import retrieve_site_by_slug

LOGGER = logging.getLogger(KEY_ENERGY)
BAUDS = 57600


class Command(AbstractCommand):
    """Command class
    """
    help = "Retrieve Currentcost data from Currentcost EnviR 128"
    out = sys.stdout
    name = "Currentcost connector"
    logger = LOGGER

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('site_id', type=str, help='Define site_id for this command')
        parser.add_argument('variable_id', type=str, help='Define variable_id for this command')
        parser.add_argument('tty_port', type=str, help='Define tty_port for this command')
        # Named (optional) arguments
        parser.add_argument(
            '--timeout', action='store', dest="timeout", default=10, type=int, help='Define timeout for this command')
        parser.add_argument(
            '--usb_retry', action='store', dest="usb_retry", default=5, type=int, help='Define usb_retry for this cmd')
        parser.add_argument(
            '--break_loop', action='store_true', dest="break_loop", default=False, help='Break the infinite loop')

    def run(self, *args, **options):
        self.site_id = options["site_id"]
        variable_id = options["variable_id"]
        tty_port = options["tty_port"]
        timeout = options["timeout"]
        usb_retry = options["usb_retry"]
        break_loop = options["break_loop"]
        ser_connection = None
        infinite_loop = True
        while infinite_loop:
            if break_loop:
                infinite_loop = False
            try:
                # If we are not connected to TTY port
                if ser_connection is None:
                    ser_connection = serial.Serial(tty_port, BAUDS, timeout=timeout)
                    self.send_error(TTY_CONNECTION_SUCCESS % (variable_id, self.site_id, tty_port))
                # If we are connected to TTY port
                if ser_connection is not None:
                    # We wait for a new message on this socket
                    data = ser_connection.readline()
                    # If we reach timeout
                    if len(data) == 0:
                        error = ERROR_CURRENTCOST[ERROR_CC_NO_MESSAGE] % (variable_id, self.site_id)
                        self.send_error(error)
                        continue
                    # data_date = datetime.utcnow().isoformat('T')
                    # data_dst_timezone = tzname[1]
                    # data_non_dst_timezone = tzname[0]
                    # # We parse the result
                    # topic, message = data_validator(data, variable_id, site_id)
                    # message = {
                    #     "siteID": site_id,
                    #     "variableID": variable_id,
                    #     "value": message,
                    #     "date": data_date,
                    #     "dstTimezone": data_dst_timezone,
                    #     "nonDstTimezone": data_non_dst_timezone
                    # }

                    # topic, message, series = get_currentcost_message(
                    #     topic, message, data, timeseries_args, data_folder)

                    # # We send message
                    # messager.send(topic, message)

                    # for serie in series:
                    #     # We send JSON series
                    #     messager.send(
                    #         TIMESERIES,
                    #         json.dumps(serie))
            # If during this process, someone deactivate USB connection
            except (OSError, serial.serialutil.SerialException):
                # If we are connected                    
                if ser_connection is not None:
                    # We reinit serial connection
                    ser_connection.close()
                    ser_connection = None
                    # And we log this error
                    error = ERROR_CURRENTCOST[ERROR_CC_NO_MESSAGE] % (variable_id, self.site_id)
                    self.send_error(error)
                # Else
                else:
                    # We send this error
                    error = ERROR_CURRENTCOST[ERROR_CC_BAD_PORT] % (variable_id, self.site_id, tty_port, usb_retry)
                    self.send_error(error)
                    sleep(usb_retry)
