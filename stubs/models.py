#!/usr/bin/python3
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""File that define Stubs models"""

from django.db import models


class StubsAPIOpening(models.Model):
    """StubsAPIOpening model
    """
    open_metear_api = models.BooleanField(blank=True, default=False)
