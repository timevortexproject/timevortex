#!/usr/bin/python3
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""File that define Admin fields"""

from django.contrib import admin
from weather import models


class SettingsAdmin(admin.ModelAdmin):
    """SiteAdmin class
    """
    list_display = ('label', 'slug', 'value')
    list_filter = ('label', 'slug', 'value')
    search_fields = ('label', 'slug')


admin.site.register(models.Settings, SettingsAdmin)
