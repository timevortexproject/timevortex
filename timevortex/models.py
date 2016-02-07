#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

from django.db import models
from django.core.exceptions import ValidationError
# from timevortex.utils.globals import LOGGER

EXCEPTION_VARIABLES_PAST_DATE = "Date are in the past"
APP_NAME = "timevortex"


class Site(models.Model):
    """Site model.
    """
    NO_TYPE = '0'
    METEAR_TYPE = '1'
    HOME_TYPE = '2'
    SITE_TYPE_CHOICES = (
        (NO_TYPE, 'Pas de type particulier'),
        (METEAR_TYPE, 'METEAR'),
        (HOME_TYPE, 'HOME_TYPE'),
    )

    label = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    site_type = models.CharField(
        max_length=2,
        choices=SITE_TYPE_CHOICES,
        null=True,
        blank=True
    )

    class Meta:
        app_label = APP_NAME

    def __str__(self):
        return self.label


class Variable(models.Model):
    """Variables model.
    """
    site = models.ForeignKey(Site)
    label = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    start_date = models.DateTimeField(null=True, blank=True)
    start_value = models.TextField(blank=True, null=True)
    end_date = models.DateTimeField(null=True, blank=True)
    end_value = models.TextField(blank=True, null=True)

    def update_value(self, date, value):
        """Update value
        """
        if date > self.end_date:
            self.end_date = date
            self.end_value = value
        elif date < self.start_date:
            self.start_date = date
            self.start_value = value
        else:
            raise ValidationError(EXCEPTION_VARIABLES_PAST_DATE)
        if self.start_date is None:
            self.start_date = date
            self.start_value = value

    class Meta:
        app_label = APP_NAME

    def __str__(self):
        return self.label


def get_sites_by_type(site_type=Site.NO_TYPE):
    try:
        return Site.objects.filter(site_type=site_type)
    except Site.DoesNotExist:
        return []


def get_site_by_slug(slug):
    try:
        return Site.objects.filter(slug=slug)
    except Site.DoesNotExist:
        return None


def get_site_by_slug_and_type(slug, site_type):
    try:
        return Site.objects.filter(slug=slug, site_type=site_type)
    except Site.DoesNotExist:
        return None
