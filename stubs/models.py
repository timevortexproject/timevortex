#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

from django.db import models


class StubsAPIOpening(models.Model):
    open_metear_api = models.BooleanField(blank=True, default=False)
