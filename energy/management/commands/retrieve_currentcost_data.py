#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""Currentcost command"""

import sys
import serial
import logging
from time import sleep
from xml.etree import ElementTree
from django.utils import timezone
from energy.utils.globals import KEY_ENERGY, ERROR_CURRENTCOST, ERROR_CC_NO_MESSAGE, ERROR_CC_BAD_PORT
from energy.utils.globals import TTY_CONNECTION_SUCCESS, ERROR_CC_DISCONNECTED, ERROR_CC_INCORRECT_MESSAGE
from energy.utils.globals import CURRENTCOST_UNICODE_ERROR, ERROR_CC_INCORRECT_MESSAGE_MISSING_TMPR
from energy.utils.globals import ERROR_CC_INCORRECT_MESSAGE_MISSING_WATTS
from timevortex.utils.commands import AbstractCommand
from timevortex.utils.globals import timeseries_json
from timevortex.models import get_site_by_slug, create_site, Site, update_or_create_variable

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
        parser.add_argument('--ch1_kwh', action='store', dest="ch1_kwh", default=None, type=str, help='Affect name to ch1_kwh')
        parser.add_argument('--ch2', action='store', dest="ch2", default=None, type=str, help='Affect name to ch2')
        parser.add_argument('--ch2_kwh', action='store', dest="ch2_kwh", default=None, type=str, help='Affect name to ch2_kwh')
        parser.add_argument('--ch3', action='store', dest="ch3", default=None, type=str, help='Affect name to ch3')
        parser.add_argument('--ch3_kwh', action='store', dest="ch3_kwh", default=None, type=str, help='Affect name to ch3_kwh')
        parser.add_argument('--tmpr', action='store', dest="tmpr", default=None, type=str, help='Affect name to tmpr')

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
        ch1_kwh = options["ch1_kwh"]
        ch2_kwh = options["ch2_kwh"]
        ch3_kwh = options["ch3_kwh"]
        tmpr = options["tmpr"]
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
                    date_readline = timezone.now()
                    # We get a clean xml and channel values
                    cc_xml, ch1_w, ch2_w, ch3_w, temperature, hist = convert_cc_xml_to_dict(cc_xml)
                    # We log current xml message for hard recovery
                    self.log_error(timeseries_json(self.site_id, "cc_xml", cc_xml, date_readline.isoformat()))
                    # For each channel, we update value in DB and send timeseries signal
                    #
                    # Todo: compute kwh, log history
                    #
                    site = get_site_by_slug(self.site_id)
                    if site is None:
                        site = create_site(slug=self.site_id, site_type=Site.HOME_TYPE)
                    if ch1 is not None and ch1_w is not None:
                        variable_ch1 = update_or_create_variable(site=site, slug=ch1, date=date_readline, value=ch1_w)
                        self.send_timeseries(timeseries_json(self.site_id, ch1, ch1_w, date_readline.isoformat()))
                        if ch1_kwh:
                            ch1_kwh_value = "0.0"
                            update_or_create_variable(site=site, slug=ch1_kwh, date=date_readline, value=ch1_kwh_value)
                            self.send_timeseries(
                                timeseries_json(self.site_id, ch1_kwh, ch1_kwh_value, date_readline.isoformat()))
                    if ch2 is not None and ch2_w is not None:
                        variable_ch2 = update_or_create_variable(site=site, slug=ch2, date=date_readline, value=ch2_w)
                        self.send_timeseries(timeseries_json(self.site_id, ch2, ch2_w, date_readline.isoformat()))
                        if ch2_kwh:
                            ch2_kwh_value = "0.0"
                            update_or_create_variable(site=site, slug=ch2_kwh, date=date_readline, value=ch2_kwh_value)
                            self.send_timeseries(
                                timeseries_json(self.site_id, ch2_kwh, ch2_kwh_value, date_readline.isoformat()))
                    if ch3 is not None and ch3_w is not None:
                        variable_ch3 = update_or_create_variable(site=site, slug=ch3, date=date_readline, value=ch3_w)
                        self.send_timeseries(timeseries_json(self.site_id, ch3, ch3_w, date_readline.isoformat()))
                        if ch3_kwh:
                            ch3_kwh_value = "0.0"
                            update_or_create_variable(site=site, slug=ch3_kwh, date=date_readline, value=ch3_kwh_value)
                            self.send_timeseries(
                                timeseries_json(self.site_id, ch3_kwh, ch3_kwh_value, date_readline.isoformat()))
                    if tmpr is not None and temperature is not None:
                        update_or_create_variable(site=site, slug=tmpr, date=date_readline, value=temperature)
                        self.send_timeseries(
                            timeseries_json(self.site_id, tmpr, temperature, date_readline.isoformat()))

                    
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
