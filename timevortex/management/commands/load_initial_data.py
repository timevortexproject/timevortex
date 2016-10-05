#!/usr/bin/python3
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""Insert initial data if not exist"""

import logging
from django.core import management
from django.contrib.auth.models import User
from timevortex.utils.commands import AbstractCommand
from weather.models import set_metear_start_date, get_metear_start_date
from timevortex.models import get_next_send_daily_report, set_next_send_daily_report, get_backup_target_folder
from timevortex.models import set_backup_target_folder

LOGGER = logging.getLogger("timevortex")
MAIN_HELP_TEXT = "Insert initial data if not exist"


class Command(AbstractCommand):
    """Command class
    """
    help = MAIN_HELP_TEXT
    name = "load initial data command"
    logger = LOGGER
    sleep_time = 0

    def run(self, *args, **options):
        """Run
        """
        self.infinite_loop = False
        # Sites
        management.call_command('loaddata', "initial_data/sites.json", database="default", verbosity=1)
        # Users
        username = "timevortex"
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            management.call_command('createsuperuser', username=username, email="default_admin@timevortexproject.org",
                                    database="default", verbosity=1, interactive=False)
            superuser = User.objects.get(username=username)
            superuser.password = "pbkdf2_sha256$24000$kYOdQmhikXc5$itTc4NMpkkXbA37CGLZoRciyvzb35/kXDXgnAI5Fw5A="
            superuser.save()
        # Timevortex settings
        if get_next_send_daily_report() is None:
            set_next_send_daily_report('86359')
        if get_backup_target_folder() is None:
            set_backup_target_folder('../common/backup')
        # Weather settings
        if get_metear_start_date() is None:
            set_metear_start_date('2010-01-01')
