#!/usr/bin/python3
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""File that define Admin fields"""

from django.contrib import admin
from energy import models


class CurrentCostSettingsAdmin(admin.ModelAdmin):
    """SiteAdmin class
    """
    list_display = (
        'currentcost_variable', 'ch1_variable', 'ch1_kwh_variable', 'ch2_variable', 'ch2_kwh_variable',
        'ch3_variable', 'ch3_kwh_variable', 'tmpr_variable', 'tty_port', 'timeout', 'usb_retry')
    list_filter = (
        'currentcost_variable', 'ch1_variable', 'ch1_kwh_variable', 'ch2_variable', 'ch2_kwh_variable',
        'ch3_variable', 'ch3_kwh_variable', 'tmpr_variable', 'tty_port')
    search_fields = (
        'currentcost_variable', 'ch1_variable', 'ch1_kwh_variable', 'ch2_variable', 'ch2_kwh_variable',
        'ch3_variable', 'ch3_kwh_variable', 'tmpr_variable', 'tty_port')


admin.site.register(models.CurrentCostSetting, CurrentCostSettingsAdmin)
