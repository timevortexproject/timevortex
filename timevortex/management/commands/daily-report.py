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

KEY_DEFAULT_FROM_EMAIL = "DEFAULT_FROM_EMAIL"
DEFAULT_DEFAULT_FROM_EMAIL = "Timevortex <phase.test.email@gmail.com>"

# Expected params
#   Active or not
#   Email params
#   email target
#   site_id impacted

def send_daily_report_email(report):
    """Send daily report email
    """
    emails = ['pierreleray64@gmail.com']
    subject = render_to_string("emails/daily_report/subject.txt", report)
    body = render_to_string("emails/daily_report/full.txt", report)
    body_html = render_to_string("emails/daily_report/full.html", report)
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
    f = open(temp_file, 'r')
    free = f.readlines()
    f.close()
    free = ''.join(free)
    return free[:-1]


class Command(BaseCommand):
    """Command class
    """

    help = "Daily report command that send email"

    def handle(self, *args, **options):
        report = {
            "yesterday_date": (timezone.now() - timedelta(days=1)).strftime("%d-%m-%Y"),
            "free_space": collect_free_space(),
            "sites": [
                {
                    "name": "system",
                    "errorNumbers": 0
                }, {
                    "name": "liogen_home",
                    "errorNumbers": 364,
                    "seriesNumbers": sorted([
                        ("living_room_temperature", 1335),
                        ("main_consumption_watts", 10354),
                        ("main_consumption_kwh", 10354)])
                }
            ]
        }

        send_daily_report_email(report)

