#!/usr/bin/python3
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""File that define Timevortex model"""

from django.db import models
from django.core.exceptions import ValidationError
from timevortex.utils.globals import KEY_SENDER_EMAIL, KEY_SENDER_PASSWORD, KEY_TARGET_INFORMATION_EMAIL, LOGGER
from timevortex.utils.globals import KEY_NEXT_SEND_DAILY_REPORT, KEY_LAST_TIME_DAILY_REPORT

EXCEPTION_VARIABLES_PAST_DATE = "Date are in the past"
APP_NAME = "timevortex"
BACKUP_TARGET_FOLDER = "backup_target_folder"


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
        # LOGGER.info(self.slug)
        # LOGGER.info(self.start_date)
        # LOGGER.info(self.start_value)
        # LOGGER.info(self.end_date)
        # LOGGER.info(self.end_value)
        # LOGGER.info(date)
        # LOGGER.info(value)
        if self.end_date is None or date > self.end_date:
            self.end_date = date
            self.end_value = value
        elif self.start_date is None or date < self.start_date:
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


def get_backup_target_folder():
    try:
        return Setting.objects.get(slug=BACKUP_TARGET_FOLDER).value
    except Setting.DoesNotExist:
        return None


def set_backup_target_folder(new_folder):
    try:
        settings = Setting.objects.get(slug=BACKUP_TARGET_FOLDER)
        settings.value = new_folder
        settings.save()
    except Setting.DoesNotExist:
        Setting.objects.create(
            label=BACKUP_TARGET_FOLDER,
            slug=BACKUP_TARGET_FOLDER,
            value=new_folder)


def get_sites_by_type(site_type=Site.NO_TYPE):
    """Get site by type
    """
    try:
        return Site.objects.filter(site_type=site_type)
    except Site.DoesNotExist:
        return []


def get_site_by_slug(slug):
    """Get site by slug
    """
    try:
        return Site.objects.get(slug=slug)
    except Site.DoesNotExist:
        return None


def get_site_by_slug_and_type(slug, site_type):
    """Get site by slug and type
    """
    try:
        return Site.objects.get(slug=slug, site_type=site_type)
    except Site.DoesNotExist:
        return None


def create_site(slug, site_type, label=None):
    """Create site
    """
    return Site.objects.create(slug=slug, site_type=site_type, label=label)


def create_variable(site, label, slug):
    """Create variable
    """
    return Variable.objects.create(site=site, label=label, slug=slug)


def update_or_create_variable(site, slug, date, value):
    """Update or create variable
    """
    variable = None
    try:
        variable = Variable.objects.get(site=site, slug=slug)
        variable.update_value(date, value)
        variable.save()
    except Variable.DoesNotExist:
        LOGGER.info("Variable creation %s", slug)
        variable = Variable.objects.create(
            site=site,
            slug=slug,
            label=slug,
            start_date=date,
            start_value=value,
            end_date=date,
            end_value=value)
    except ValidationError:
        variable = None
    return variable


def get_variable_by_slug(site, slug):
    """Get variable by slug
    """
    try:
        return Variable.objects.get(site=site, slug=slug)
    except Variable.DoesNotExist:
        return None


def get_site_variables(site):
    """Get variables of a site
    """
    return Variable.objects.filter(site=site)


def get_sender_email():
    """Get sender email
    """
    try:
        return Setting.objects.get(slug=KEY_SENDER_EMAIL)
    except Setting.DoesNotExist:
        return None


def get_sender_password():
    """Get sender password
    """
    try:
        return Setting.objects.get(slug=KEY_SENDER_PASSWORD)
    except Setting.DoesNotExist:
        return None


def get_target_email():
    """Get target email
    """
    try:
        return Setting.objects.get(slug=KEY_TARGET_INFORMATION_EMAIL)
    except Setting.DoesNotExist:
        return None


def get_next_send_daily_report():
    """Get next send daily report
    """
    try:
        return Setting.objects.get(slug=KEY_NEXT_SEND_DAILY_REPORT)
    except Setting.DoesNotExist:
        return None


def set_next_send_daily_report(value):
    """Set next send daily report
    """
    try:
        settings = Setting.objects.get(slug=KEY_NEXT_SEND_DAILY_REPORT)
        settings.value = value
        settings.save()
    except Setting.DoesNotExist:
        Setting.objects.create(
            label=KEY_NEXT_SEND_DAILY_REPORT,
            slug=KEY_NEXT_SEND_DAILY_REPORT,
            value=value
        )


def get_last_time_daily_report():
    """Get last time daily report
    """
    try:
        return Setting.objects.get(slug=KEY_LAST_TIME_DAILY_REPORT)
    except Setting.DoesNotExist:
        return None


def create_last_time_daily_report(label, slug, value):
    """Create last time daily report
    """
    return Setting.objects.create(label=label, slug=slug, value=value)
