#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""Currentcost command"""

import sys
import serial
import logging
from time import sleep
from xml.etree import ElementTree
from energy.utils.globals import KEY_ENERGY, ERROR_CURRENTCOST, ERROR_CC_NO_MESSAGE, ERROR_CC_BAD_PORT
from energy.utils.globals import TTY_CONNECTION_SUCCESS, ERROR_CC_DISCONNECTED, ERROR_CC_INCORRECT_MESSAGE
from energy.utils.globals import CURRENTCOST_UNICODE_ERROR, ERROR_CC_INCORRECT_MESSAGE_MISSING_TMPR
from energy.utils.globals import ERROR_CC_INCORRECT_MESSAGE_MISSING_WATTS
from timevortex.utils.commands import AbstractCommand
# from timevortex.models import retrieve_site_by_slug

LOGGER = logging.getLogger(KEY_ENERGY)
BAUDS = 57600


class ExceptionWithValue(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class CCNoMessage(Exception):
    pass


class CCNoTmpr(ExceptionWithValue):
    pass


class CCNoWatts(ExceptionWithValue):
    pass


class CCIncorrectData(ExceptionWithValue):
    pass


def convert_cc_xml_to_dict(cc_xml):
    """Analyse data from currentcost and return according TOPIC and MESSAGE.

    :param data: XML string that contain data.
    :type variable_id: str.

    :returns:  str -- Topic of the message (error or success) and
        Message containing error description or data sent by CC.

    """
    if len(cc_xml) == 0:
        raise CCNoMessage

    try:
        cc_xml = cc_xml.decode("utf-8").replace("\n", "").replace("\r", "")
        cc_xml_parsed = ElementTree.fromstring(cc_xml)
    except UnicodeDecodeError:
        raise CCIncorrectData(CURRENTCOST_UNICODE_ERROR)
    except ElementTree.ParseError:
        raise CCIncorrectData(cc_xml)

    ch1_w = None
    ch2_w = None
    ch3_w = None
    temperature = cc_xml_parsed.findtext("tmpr")
    hist = cc_xml_parsed.findtext("hist")
    if hist is None:
        if temperature is None:
            raise CCNoTmpr(cc_xml)
        else:
            temperature = float(temperature)
            if cc_xml_parsed.find("ch1") is not None:
                ch1_w = float(cc_xml_parsed.find("ch1").findtext("watts"))
            if cc_xml_parsed.find("ch2") is not None:
                ch2_w = float(cc_xml_parsed.find("ch2").findtext("watts"))
            if cc_xml_parsed.find("ch3") is not None:
                ch3_w = float(cc_xml_parsed.find("ch3").findtext("watts"))
            if ch1_w is None and ch2_w is None and ch3_w is None:
                raise CCNoWatts(cc_xml)
    else:
        hist = True

    return cc_xml, ch1_w, ch2_w, ch3_w, temperature, hist


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
        parser.add_argument('--ch1', action='store', dest="ch1", default=None, type=str, help='Affect name to ch1')
        parser.add_argument('--ch2', action='store', dest="ch2", default=None, type=str, help='Affect name to ch2')
        parser.add_argument('--ch3', action='store', dest="ch3", default=None, type=str, help='Affect name to ch3')

    def run(self, *args, **options):
        self.site_id = options["site_id"]
        variable_id = options["variable_id"]
        tty_port = options["tty_port"]
        timeout = options["timeout"]
        usb_retry = options["usb_retry"]
        break_loop = options["break_loop"]
        ch1 = options["ch1"]
        ch2 = options["ch2"]
        ch3 = options["ch3"]
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
                    cc_xml = ser_connection.readline()
                    cc_xml, ch1_w, ch2_w, ch3_w, temperature, hist = convert_cc_xml_to_dict(cc_xml)
                    self.log_error(cc_xml)
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
            except CCNoMessage:
                error = ERROR_CURRENTCOST[ERROR_CC_NO_MESSAGE] % (variable_id, self.site_id)
                self.send_error(error)
            except CCIncorrectData as err:
                error = ERROR_CURRENTCOST[ERROR_CC_INCORRECT_MESSAGE] % (variable_id, self.site_id, err.value)
                self.send_error(error)
            except CCNoTmpr as err:
                error = ERROR_CURRENTCOST[ERROR_CC_INCORRECT_MESSAGE_MISSING_TMPR] % (
                    variable_id, self.site_id, err.value)
                self.send_error(error)
            except CCNoWatts as err:
                error = ERROR_CURRENTCOST[ERROR_CC_INCORRECT_MESSAGE_MISSING_WATTS] % (
                    variable_id, self.site_id, err.value)
                self.send_error(error)
            except (OSError, serial.serialutil.SerialException):
                # if we are connected
                if ser_connection is not None:
                    # We reinit serial connection
                    ser_connection.close()
                    ser_connection = None
                    # And we log this error
                    error = ERROR_CURRENTCOST[ERROR_CC_DISCONNECTED] % (variable_id, self.site_id, tty_port)
                    self.send_error(error)
                # Else
                else:
                    # We send this error
                    error = ERROR_CURRENTCOST[ERROR_CC_BAD_PORT] % (variable_id, self.site_id, tty_port, usb_retry)
                    self.send_error(error)
                    sleep(usb_retry)
