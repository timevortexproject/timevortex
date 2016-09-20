#!/usr/bin/python3
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""File that define admin fields"""

from django.contrib import admin
from stubs import models


class StubsAPIOpeningAdmin(admin.ModelAdmin):
    """StubsAPIOpeningAdmin model
    """
    list_display = ('open_metear_api',)

admin.site.register(models.StubsAPIOpening, StubsAPIOpeningAdmin)
