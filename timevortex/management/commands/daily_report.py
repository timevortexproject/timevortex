#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""Daily report command that send email"""

import os
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from timevortex.utils.filestorage import FILE_STORAGE_SPACE

# Data storage


# Email sender
KEY_DEFAULT_FROM_EMAIL = "DEFAULT_FROM_EMAIL"
DEFAULT_DEFAULT_FROM_EMAIL = "Timevortex <phase.test.email@gmail.com>"

# Emaill template
FILE_EMAIL_SUBJECT = "emails/daily_report/subject.txt"
FILE_EMAIL_BODY_TXT = "emails/daily_report/full.txt"
FILE_EMAIL_BODY_HTML = "emails/daily_report/full.html"

# KEY
KEY_REPORT_NAME = "name"
KEY_REPORT_ERROR_NUMBERS = "errorNumbers"
KEY_REPORT_SERIES_NUMBERS = "seriesNumbers"


def send_daily_report_email(emails, report):
    """Send daily report email
    """
    subject = render_to_string(FILE_EMAIL_SUBJECT, report)
    body = render_to_string(FILE_EMAIL_BODY_TXT, report)
    body_html = render_to_string(FILE_EMAIL_BODY_HTML, report)
    sender_email = getattr(settings, KEY_DEFAULT_FROM_EMAIL, DEFAULT_DEFAULT_FROM_EMAIL)

    msg = EmailMultiAlternatives(subject, body, sender_email, emails)
    msg.attach_alternative(body_html, "text/html")
    msg.content_subtype = "plain"
    msg.send()


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


class Command(BaseCommand):
    """Command class
    """

    help = "Daily report command that send email"

    def handle(self, *args, **options):
        day_date = (timezone.now() - timedelta(days=1))
        report = {
            "yesterday_date": day_date.strftime("%d-%m-%Y"),
            "free_space": collect_free_space(),
            "sites": get_sites_information(day_date.strftime("%Y-%m-%d"))
        }

        emails = ['pierreleray64@gmail.com']

        send_daily_report_email(emails, report)
