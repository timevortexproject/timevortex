#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

from django.contrib import admin
from stubs import models


class StubsAPIOpeningAdmin(admin.ModelAdmin):
    list_display = ('open_metear_api',)

admin.site.register(models.StubsAPIOpening, StubsAPIOpeningAdmin)
