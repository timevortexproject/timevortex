#!/usr/bin/python3
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""File that define Weather model"""

from django.db import models

APP_NAME = "weather"
METEAR_START_DATE = "metear_start_date"


class Setting(models.Model):
    """Site model.
    """
    label = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    value = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        app_label = APP_NAME

    def __str__(self):
        return self.label


def get_metear_start_date():
    try:
        return Setting.objects.get(slug=METEAR_START_DATE).value
    except Setting.DoesNotExist:
        return None


def set_metear_start_date(new_date):
    try:
        settings = Setting.objects.get(slug=METEAR_START_DATE)
        settings.value = new_date
        settings.save()
    except Setting.DoesNotExist:
        Setting.objects.create(
            label=METEAR_START_DATE,
            slug=METEAR_START_DATE,
            value=new_date)
