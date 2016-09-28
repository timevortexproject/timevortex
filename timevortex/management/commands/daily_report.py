#!/usr/bin/python3
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""Daily report command that send email"""

import os
import pytz
import logging
import dateutil.parser
from datetime import timedelta, datetime
from smtplib import SMTPAuthenticationError
from django.utils import timezone
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from timevortex.models import Setting
from timevortex.utils.commands import AbstractCommand
from timevortex.utils.filestorage import FILE_STORAGE_SPACE
from timevortex.utils.globals import KEY_SENDER_EMAIL, KEY_SENDER_PASSWORD, KEY_TARGET_INFORMATION_EMAIL
from timevortex.utils.globals import KEY_NEXT_SEND_DAILY_REPORT, KEY_LAST_TIME_DAILY_REPORT, ERROR_TIMEVORTEX
from timevortex.utils.globals import ERROR_MISSING_SENDER_EMAIL, KEY_EMAIL_HOST_USER, ERROR_SMTP_AUTH
from timevortex.utils.globals import ERROR_MISSING_SENDER_PASSWORD, KEY_EMAIL_HOST_PASSWORD, ERROR_MISSING_TARGET_EMAIL
from timevortex.utils.globals import ERROR_MISSING_NEXT_SEND, LABEL_LAST_TIME_DAILY_REPORT

# Data storage
LOGGER = logging.getLogger("timevortex")

# Email sender
KEY_DEFAULT_FROM_EMAIL = "DEFAULT_FROM_EMAIL"
DEFAULT_DEFAULT_FROM_EMAIL = "Timevortex <%s@gmail.com>"

# Emaill template
FILE_EMAIL_SUBJECT = "emails/daily_report/subject.txt"
FILE_EMAIL_BODY_TXT = "emails/daily_report/full.txt"
FILE_EMAIL_BODY_HTML = "emails/daily_report/full.html"

# KEY
KEY_REPORT_NAME = "name"
KEY_REPORT_ERROR_NUMBERS = "errorNumbers"
KEY_REPORT_SERIES_NUMBERS = "seriesNumbers"


def collect_free_space():
    """This method collect free space on disk.

    :returns: str -- Str containing free space.

    """
    temp_file = "/tmp/freespace.log"
    os.system('df -h / > %s' % temp_file)
    file_desc = open(temp_file, 'r')
    free = file_desc.readlines()
    file_desc.close()
    free = ''.join(free)
    return free[:-1].replace("\n", "<br/>")


def get_sites_information(day_date):
    """Get site information
    """
    sites = []
    sites_list = FILE_STORAGE_SPACE.get_sites_list()
    for site_id in sites_list:
        site_info = {
            KEY_REPORT_NAME: site_id,
            KEY_REPORT_ERROR_NUMBERS: FILE_STORAGE_SPACE.get_number_of_error(site_id, day_date),
            KEY_REPORT_SERIES_NUMBERS: FILE_STORAGE_SPACE.get_number_of_series(site_id, day_date)
        }
        sites.append(site_info)

    return sites


class Command(AbstractCommand):
    """Command class

        Test cases:
            * No sender_email in DB => log error ERROR_MISSING_SENDER_EMAIL
            * No sender_password in DB => log error ERROR_MISSING_SENDER_PASSWORD
            * Bad SMTP authentication => log error ERROR_SMTP_AUTH
    """

    help = "Daily report command that send email"
    name = "daily report command"
    logger = LOGGER
    sleep_time = 300
    sender_email = None
    sender_password = None

    def send_daily_report_email(self, emails, report):
        """Send daily report email
        """
        subject = render_to_string(FILE_EMAIL_SUBJECT, report)
        body = render_to_string(FILE_EMAIL_BODY_TXT, report)
        body_html = render_to_string(FILE_EMAIL_BODY_HTML, report)
        header_email = DEFAULT_DEFAULT_FROM_EMAIL % self.sender_email.value

        msg = EmailMultiAlternatives(subject, body, header_email, emails)
        msg.attach_alternative(body_html, "text/html")
        msg.content_subtype = "plain"
        try:
            msg.send()
        except SMTPAuthenticationError:
            error_msg = ERROR_TIMEVORTEX[ERROR_SMTP_AUTH] % (self.sender_email.value, self.sender_password)
            self.logger.error(error_msg)

    def run(self, *args, **options):
        target_email = None
        next_send_daily_report = None
        last_time_daily_report = None
        last_time_daily_report_datetime = None
        now = timezone.now()
        try:
            self.sender_email = Setting.objects.get(slug=KEY_SENDER_EMAIL)
            self.sender_password = Setting.objects.get(slug=KEY_SENDER_PASSWORD)
            target_email = Setting.objects.get(slug=KEY_TARGET_INFORMATION_EMAIL)
            next_send_daily_report = Setting.objects.get(slug=KEY_NEXT_SEND_DAILY_REPORT)
            last_time_daily_report = Setting.objects.get(slug=KEY_LAST_TIME_DAILY_REPORT)
            last_time_daily_report_datetime = dateutil.parser.parse(last_time_daily_report.value).replace(
                tzinfo=pytz.UTC)
        except Setting.DoesNotExist:
            if self.sender_email is None:
                self.logger.error(ERROR_TIMEVORTEX[ERROR_MISSING_SENDER_EMAIL])
            elif self.sender_password is None:
                self.logger.error(ERROR_TIMEVORTEX[ERROR_MISSING_SENDER_PASSWORD])
            elif target_email is None:
                self.logger.error(ERROR_TIMEVORTEX[ERROR_MISSING_TARGET_EMAIL])
            elif next_send_daily_report is None:
                self.logger.error(ERROR_TIMEVORTEX[ERROR_MISSING_NEXT_SEND])
            elif last_time_daily_report_datetime is None:
                last_time_daily_report_datetime = (datetime.now() - timedelta(days=1)).replace(hour=4, minute=0,
                                                                                               second=0, microsecond=0)
                Setting.objects.create(label=LABEL_LAST_TIME_DAILY_REPORT, slug=KEY_LAST_TIME_DAILY_REPORT,
                                       value=last_time_daily_report_datetime)
            return

        setattr(settings, KEY_EMAIL_HOST_USER, self.sender_email.value)
        setattr(settings, KEY_EMAIL_HOST_PASSWORD, self.sender_password.value)

        if now >= last_time_daily_report_datetime + timedelta(seconds=int(next_send_daily_report.value)):

            # get last_time_daily_report from DB
            day_date = (timezone.now() - timedelta(days=1))
            report = {
                "yesterday_date": day_date.strftime("%d-%m-%Y"),
                "free_space": collect_free_space(),
                "sites": get_sites_information(day_date.strftime("%Y-%m-%d"))
            }

            emails = [target_email.value]

            self.send_daily_report_email(emails, report)

            last_time_daily_report.value = now
            last_time_daily_report.save()
