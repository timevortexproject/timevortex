#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""Timevortex signals definition"""

import json
from django.dispatch import Signal, receiver
from timevortex.utils.globals import KEY_SITE_ID, KEY_VARIABLE_ID, KEY_VALUE, KEY_DATE, KEY_DST_TIMEZONE
from timevortex.utils.globals import KEY_NON_DST_TIMEZONE, KEY_TIMESERIES, KEY_ERROR
from timevortex.utils.timeserieslogger import ERROR_TSL, KEY_TSL_NO_NON_DST_TIMEZONE, KEY_TSL_NO_DST_TIMEZONE
from timevortex.utils.timeserieslogger import KEY_TSL_NO_VALUE, KEY_TSL_NO_VARIABLE_ID, KEY_TSL_NO_SITE_ID
from timevortex.utils.timeserieslogger import KEY_TSL_NO_DATE, KEY_TSL_BAD_JSON
from timevortex.utils.filestorage import FILE_STORAGE_SPACE


SIGNAL_TIMESERIES = Signal(providing_args=[KEY_TIMESERIES])


def validate_message(message):
    """Method that validate entrance message.

        :param message: Message receive through RabbitMQ in JSON.
        :type topic: str.
    """
    raised_error = None
    validated_message = None

    try:
        validated_message = json.loads(message)
        if KEY_SITE_ID not in validated_message:
            raised_error = ERROR_TSL[KEY_TSL_NO_SITE_ID] % message
        elif KEY_VARIABLE_ID not in validated_message:
            raised_error = ERROR_TSL[KEY_TSL_NO_VARIABLE_ID] % message
        elif KEY_VALUE not in validated_message:
            raised_error = ERROR_TSL[KEY_TSL_NO_VALUE] % message
        elif KEY_DATE not in validated_message:
            raised_error = ERROR_TSL[KEY_TSL_NO_DATE] % message
        elif KEY_DST_TIMEZONE not in validated_message:
            raised_error = ERROR_TSL[KEY_TSL_NO_DST_TIMEZONE] % message
        elif KEY_NON_DST_TIMEZONE not in validated_message:
            raised_error = ERROR_TSL[KEY_TSL_NO_NON_DST_TIMEZONE] % message
    except ValueError:
        raised_error = ERROR_TSL[KEY_TSL_BAD_JSON] % message

    return raised_error, validated_message


@receiver(SIGNAL_TIMESERIES)
def timeseries_receiver(sender, **kwargs):  # pylint: disable=I0011,W0613
    """Receiver method for timeseries signal
    """
    timeseries = ""
    if KEY_TIMESERIES in kwargs:
        timeseries = kwargs[KEY_TIMESERIES]
    raised_error, validated_timeseries = validate_message(timeseries)
    if raised_error:
        FILE_STORAGE_SPACE.store_error(raised_error)
    elif validated_timeseries[KEY_VARIABLE_ID] == KEY_ERROR:
        FILE_STORAGE_SPACE.insert_error(validated_timeseries)
    else:
        FILE_STORAGE_SPACE.insert_series(validated_timeseries)

SIGNAL_TIMESERIES.connect(timeseries_receiver)
