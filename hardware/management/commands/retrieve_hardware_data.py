#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""Hardware command"""

import psutil
from timevortex.utils.commands import AbstractCommand


class Command(AbstractCommand):
    """Command class
    """
    help = "Retireve hardware data from system commands"
    name = "Hardware crawler"

    def handle(self, *args, **options):
        LOGGER.info("Command %s started", self.name)
        print(psutil.cpu_times())
        print(psutil.cpu_count())
        print(psutil.cpu_count(logical=False))
        print(psutil.cpu_percent(interval=1, percpu=True))
        LOGGER.info("Command %s stopped", self.name)
