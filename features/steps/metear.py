#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""Functionnal test for METEAR"""

from io import StringIO
from django.conf import settings
from behave import given
from features.steps.test_utils import stubs_change_api_configuration
from features.steps.test_utils import SETTINGS_BAD_METEAR_URL, SETTINGS_BAD_CONTENT_METEAR_URL
from weather.utils.globals import SETTINGS_METEAR_URL, SETTINGS_STUBS_NEW_METEAR_URL
from weather.management.commands.retrieve_metear_data import Command
from stubs.utils.globals import KEY_STUBS_OPEN_METEAR_API


@given("I add a bad metear url in settings")
def define_wrong_metear_url(context):
    setattr(settings, SETTINGS_METEAR_URL, SETTINGS_BAD_METEAR_URL)


@given("I shutdown the metear web service")
def shutdown_metear_ws(context):
    stubs_change_api_configuration({KEY_STUBS_OPEN_METEAR_API: False})


@given("I configure metear web service to generate bad content")
def define_bad_content_metear_ws(context):
    setattr(settings, SETTINGS_METEAR_URL, SETTINGS_BAD_CONTENT_METEAR_URL)


@given("new data are available")
def new_data_available(context):
    setattr(settings, SETTINGS_METEAR_URL, SETTINGS_STUBS_NEW_METEAR_URL)


@given("I run for the first time the metear script")
def run_metear_script_populate(context):
    out = StringIO()
    command = Command()
    command.out = out
    command.handle()
