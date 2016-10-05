#!/usr/bin/python3
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""File that define Timevortex model"""

from django.db import models
from timevortex.models import Variable

KEY_CURRENTCOST_VARIABLE = "currentcost_variable"
KEY_CH1_VARIABLE = "ch1_variable"
KEY_CH1_KWH_VARIABLE = "ch1_kwh_variable"
KEY_CH2_VARIABLE = "ch2_variable"
KEY_CH2_KWH_VARIABLE = "ch2_kwh_variable"
KEY_CH3_VARIABLE = "ch3_variable"
KEY_CH3_KWH_VARIABLE = "ch3_kwh_variable"
KEY_TMPR_VARIABLE = "tmpr_variable"
KEY_TTY_PORT = "tty_port"
KEY_TIMEOUT = "timeout"
KEY_USB_RETRY = "usb_retry"
APP_NAME = "energy"


class CurrentCostSetting(models.Model):
    """CurrentCostSetting model.
    """
    currentcost_variable = models.ForeignKey(Variable)
    ch1_variable = models.ForeignKey(Variable, models.SET_NULL, null=True, blank=True, related_name='ch1_variable')
    ch1_kwh_variable = models.ForeignKey(Variable, models.SET_NULL, null=True, blank=True,
                                         related_name='ch1_kwh_variable')
    ch2_variable = models.ForeignKey(Variable, models.SET_NULL, null=True, blank=True, related_name='ch2_variable')
    ch2_kwh_variable = models.ForeignKey(Variable, models.SET_NULL, null=True, blank=True,
                                         related_name='ch2_kwh_variable')
    ch3_variable = models.ForeignKey(Variable, models.SET_NULL, null=True, blank=True, related_name='ch3_variable')
    ch3_kwh_variable = models.ForeignKey(Variable, models.SET_NULL, null=True, blank=True,
                                         related_name='ch3_kwh_variable')
    tmpr_variable = models.ForeignKey(Variable, models.SET_NULL, null=True, blank=True, related_name='tmpr_variable')
    tty_port = models.CharField(max_length=200)
    timeout = models.PositiveSmallIntegerField()
    usb_retry = models.PositiveSmallIntegerField()

    class Meta:
        app_label = APP_NAME

    def __str__(self):
        return self.currentcost_variable.label


def get_all_cc_settings():
    """Get all current cost settings
    """
    return CurrentCostSetting.objects.all()


def create_cc_settings(settings):
    """Create CC settings
    """
    return CurrentCostSetting.objects.create(
        currentcost_variable=settings[KEY_CURRENTCOST_VARIABLE],
        ch1_variable=settings[KEY_CH1_VARIABLE],
        ch1_kwh_variable=settings[KEY_CH1_KWH_VARIABLE],
        ch2_variable=settings[KEY_CH2_VARIABLE],
        ch2_kwh_variable=settings[KEY_CH2_KWH_VARIABLE],
        ch3_variable=settings[KEY_CH3_VARIABLE],
        ch3_kwh_variable=settings[KEY_CH3_KWH_VARIABLE],
        tmpr_variable=settings[KEY_TMPR_VARIABLE],
        tty_port=settings[KEY_TTY_PORT],
        timeout=settings[KEY_TIMEOUT],
        usb_retry=settings[KEY_USB_RETRY]
    )


def delete_all_settings():
    """Delete all currentcost settings
    """
    for settings in get_all_cc_settings():
        settings.delete()
