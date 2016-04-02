#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""Currentcost command"""

import sys
import logging
from time import sleep
from xml.etree import ElementTree
import serial
from django.utils import timezone
from energy.utils.globals import KEY_ENERGY, ERROR_CURRENTCOST, ERROR_CC_NO_MESSAGE, ERROR_CC_BAD_PORT
from energy.utils.globals import TTY_CONNECTION_SUCCESS, ERROR_CC_DISCONNECTED, ERROR_CC_INCORRECT_MESSAGE
from energy.utils.globals import CURRENTCOST_UNICODE_ERROR, ERROR_CC_INCORRECT_MESSAGE_MISSING_TMPR
from energy.utils.globals import ERROR_CC_INCORRECT_MESSAGE_MISSING_WATTS
from timevortex.utils.commands import AbstractCommand
from timevortex.utils.globals import timeseries_json
from timevortex.models import get_site_by_slug, create_site, Site, update_or_create_variable, get_variable_by_slug

LOGGER = logging.getLogger(KEY_ENERGY)
BAUDS = 57600
KEY_CH1 = "ch1"
KEY_CH2 = "ch2"
KEY_CH3 = "ch3"
KEY_TMPR = "tmpr"
KEY_HIST = "hist"


class ExceptionWithValue(Exception):
    """ExceptionWithValue
    """
    def __init__(self, value):
        super(ExceptionWithValue, self).__init__(value)
        self.value = value

    def __str__(self):
        return repr(self.value)


class CCNoMessage(Exception):
    """CCNoMessage
    """
    pass


class CCNoTmpr(ExceptionWithValue):
    """CCNoTmpr
    """
    pass


class CCNoWatts(ExceptionWithValue):
    """CCNoWatts
    """
    pass


class CCIncorrectData(ExceptionWithValue):
    """CCIncorrectData
    """
    pass


def get_kwh_value(variable_kwh, variable_watts, actual_date):
    """Get kWh value
    """
    if (variable_kwh is not None and
            variable_watts is not None):
        last_energy_value = float(variable_kwh.end_value)
        last_energy_date = variable_kwh.end_date
        last_power_value = float(variable_watts.end_value)
        date_delta = actual_date - last_energy_date
        watts_seconds = last_power_value * date_delta.total_seconds()
        watts_hours = watts_seconds / 3600.
        kwh = watts_hours / 1000.
        last_energy_value += kwh
        return round(last_energy_value, 6)
    else:
        return 0.0


def extract_value(cc_xml, cc_xml_parsed, temperature):
    """Extract watts and celsius values
    """
    xml_value = {
        KEY_CH1: None,
        KEY_CH2: None,
        KEY_CH3: None
    }
    if temperature is None:
        raise CCNoTmpr(cc_xml)
    else:
        for channel in xml_value:
            if cc_xml_parsed.find(channel) is not None:
                xml_value[channel] = float(cc_xml_parsed.find(channel).findtext("watts"))
        xml_value[KEY_TMPR] = float(temperature)
        if xml_value[KEY_CH1] is None and xml_value[KEY_CH2] is None and xml_value[KEY_CH3] is None:
            raise CCNoWatts(cc_xml)

    return xml_value


def extract_xml_data(cc_xml, cc_xml_parsed):
    """Read XML and extract data
    """
    temperature = cc_xml_parsed.findtext(KEY_TMPR)
    hist = cc_xml_parsed.findtext(KEY_HIST)
    if hist is None:
        hist = False
        xml_value = extract_value(cc_xml, cc_xml_parsed, temperature)
    else:
        hist = True

    return cc_xml, xml_value, hist


def convert_cc_xml_to_dict(cc_xml):
    """Analyse data from currentcost and return according TOPIC and MESSAGE.

    :param cc_xml: XML string that contain data.
    :type cc_xml: str.

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

    return extract_xml_data(cc_xml, cc_xml_parsed)


class Command(AbstractCommand):
    """Command class
    """
    help = "Retrieve Currentcost data from Currentcost EnviR 128"
    out = sys.stdout
    name = "Currentcost connector"
    logger = LOGGER
    site_id = None
    ser_connection = None

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
        parser.add_argument(
            '--ch1_kwh', action='store', dest="ch1_kwh", default=None, type=str, help='Affect name to ch1_kwh')
        parser.add_argument('--ch2', action='store', dest=KEY_CH2, default=None, type=str, help='Affect name to ch2')
        parser.add_argument(
            '--ch2_kwh', action='store', dest="ch2_kwh", default=None, type=str, help='Affect name to ch2_kwh')
        parser.add_argument('--ch3', action='store', dest=KEY_CH3, default=None, type=str, help='Affect name to ch3')
        parser.add_argument(
            '--ch3_kwh', action='store', dest="ch3_kwh", default=None, type=str, help='Affect name to ch3_kwh')
        parser.add_argument('--tmpr', action='store', dest=KEY_TMPR, default=None, type=str, help='Affect name to tmpr')

    def update_and_publish(self, site, slug, date, value):
        """Update variable value and publish on network
        """
        update_or_create_variable(site=site, slug=slug, date=date, value=value)
        self.send_timeseries(timeseries_json(self.site_id, slug, value, date.isoformat()))

    def create_kwh_timeseries(self, site, kwh_channel, variable_watts, date_readline):
        """Create kWh timeseries
        """
        variable_kwh = get_variable_by_slug(site=site, slug=kwh_channel)
        new_kwh_value = get_kwh_value(variable_kwh, variable_watts, date_readline)
        update_or_create_variable(site=site, slug=kwh_channel, date=date_readline, value=new_kwh_value)
        self.send_timeseries(timeseries_json(self.site_id, kwh_channel, new_kwh_value, date_readline.isoformat()))

    def get_site(self):
        """Get site for currentcost or create it
        """
        site = get_site_by_slug(self.site_id)
        if site is None:
            site = create_site(slug=self.site_id, site_type=Site.HOME_TYPE)
        return site

    def send_watts_timeseries(self, site, channels, date_readline):
        """Send watts timeseries
        """
        for channel, watts_value, kwh_channel in channels:
            if channel is not None and watts_value is not None:
                variable_watts = get_variable_by_slug(site=site, slug=channel)
                if kwh_channel:
                    self.create_kwh_timeseries(site, kwh_channel, variable_watts, date_readline)
                self.update_and_publish(site, channel, date_readline, watts_value)

    def send_temperature_timeseries(self, site, tmpr, temperature, date_readline):
        """Send temperature timeseries
        """
        if tmpr is not None and temperature is not None:
            self.update_and_publish(site, tmpr, date_readline, temperature)

    def currentcost_timeseries_creation(self, options, values, date_readline):
        """Update variable and publish timeseries from XML message
        """
        tmpr = options[KEY_TMPR]
        ch1_w = values[KEY_CH1]
        ch2_w = values[KEY_CH2]
        ch3_w = values[KEY_CH3]
        temperature = values[KEY_TMPR]
        # For each channel, we update value in DB and send timeseries signal
        site = self.get_site()

        channels = [
            [options[KEY_CH1], ch1_w, options["ch1_kwh"]],
            [options[KEY_CH2], ch2_w, options["ch2_kwh"]],
            [options[KEY_CH3], ch3_w, options["ch3_kwh"]],
        ]

        self.send_watts_timeseries(site, channels, date_readline)
        self.send_temperature_timeseries(site, tmpr, temperature, date_readline)

    def ser_connection_none(self, tty_port, timeout, variable_id):
        """Behavior when ser_connection is None
        """
        self.ser_connection = serial.Serial(tty_port, BAUDS, timeout=timeout)
        self.send_error(TTY_CONNECTION_SUCCESS % (variable_id, self.site_id, tty_port))

    def ser_connection_not_none(self, options):
        """Behavior when ser_connection is not None
        """
        # We wait for a new message on this socket
        cc_xml = self.ser_connection.readline()
        date_readline = timezone.now()
        # We get a clean xml and channel values
        cc_xml, values, hist = convert_cc_xml_to_dict(cc_xml)
        # We log current xml message for hard recovery
        self.log_error(timeseries_json(self.site_id, "cc_xml", cc_xml, date_readline.isoformat()))
        if hist is False:
            self.currentcost_timeseries_creation(options, values, date_readline)

    def send_currentcost_error(self, error_type, variable_id, error_params=None, error_params_2=None):
        """Send currentcost error
        """
        if error_params is None:
            error = ERROR_CURRENTCOST[error_type] % (variable_id, self.site_id)
        elif error_params_2 is None:
            error = ERROR_CURRENTCOST[error_type] % (variable_id, self.site_id, error_params)
        else:
            error = ERROR_CURRENTCOST[error_type] % (variable_id, self.site_id, error_params, error_params_2)
        self.send_error(error)

    def serial_exception(self, variable_id, tty_port, usb_retry):
        """Send correct error when serial_exception occurs
        """
        # if we are connected
        if self.ser_connection is not None:
            # We reinit serial connection
            self.ser_connection.close()
            self.ser_connection = None
            # And we log this error
            self.send_currentcost_error(ERROR_CC_DISCONNECTED, variable_id, tty_port)
        # Else
        else:
            # We send this error
            self.send_currentcost_error(ERROR_CC_BAD_PORT, variable_id, tty_port, usb_retry)
            sleep(usb_retry)

    def retrieve_data(self, options, tty_port, variable_id):
        """Connect to currentcost and retrieve data
        """
        # If we are not connected to TTY port
        if self.ser_connection is None:
            self.ser_connection_none(tty_port, options["timeout"], variable_id)
        # If we are connected to TTY port
        if self.ser_connection is not None:
            self.ser_connection_not_none(options)

    def currentcost_error_management(self, options, variable_id, tty_port, usb_retry):
        """Catch currentcost potential error
        """
        try:
            self.retrieve_data(options, tty_port, variable_id)
        except CCNoMessage:
            self.send_currentcost_error(ERROR_CC_NO_MESSAGE, variable_id)
        except CCIncorrectData as err:
            self.send_currentcost_error(ERROR_CC_INCORRECT_MESSAGE, variable_id, err.value)
        except CCNoTmpr as err:
            self.send_currentcost_error(ERROR_CC_INCORRECT_MESSAGE_MISSING_TMPR, variable_id, err.value)
        except CCNoWatts as err:
            self.send_currentcost_error(ERROR_CC_INCORRECT_MESSAGE_MISSING_WATTS, variable_id, err.value)
        except (OSError, serial.serialutil.SerialException):
            self.serial_exception(variable_id, tty_port, usb_retry)

    def run(self, *args, **options):
        """Run method
        """
        self.site_id = options["site_id"]
        variable_id = options["variable_id"]
        tty_port = options["tty_port"]
        usb_retry = options["usb_retry"]
        infinite_loop = True
        while infinite_loop:
            if options["break_loop"]:
                infinite_loop = False
            self.currentcost_error_management(options, variable_id, tty_port, usb_retry)
