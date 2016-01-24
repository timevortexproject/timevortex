#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

from django.contrib import admin
from timevortex import models


class SiteAdmin(admin.ModelAdmin):
    list_display = ('label', 'slug', 'site_type')
    list_filter = ('label', 'slug', 'site_type')
    search_fields = ('label', 'slug')


class VariableAdmin(admin.ModelAdmin):
    list_display = ('site', 'label', 'slug', 'start_date', 'start_value', 'end_date', 'end_value')
    list_filter = ('site', 'label', 'slug')
    search_fields = ('label', 'slug')


admin.site.register(models.Site, SiteAdmin)
admin.site.register(models.Variable, VariableAdmin)