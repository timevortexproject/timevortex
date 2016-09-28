#!/usr/bin/python3
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""Daily backup and csv generated files"""

import logging
from django.conf import settings
from timevortex.models import get_backup_target_folder
from timevortex.utils.commands import AbstractCommand
from timevortex.utils.globals import call_and_exit, ERROR_TIMEVORTEX, ERROR_BACKUP_DEACTIVATED

LOGGER = logging.getLogger("timevortex")
MAIN_HELP_TEXT = "Invoke rsync method to copy data on a specific folder"

# cd /opt/timevortex/data/ && rsync -az liogen_home
#     liogen@192.168.0.44:/home/liogen/workspace/timevortex/timevortex.data/backup
# cd /var/log && rsync -az timevortex liogen@192.168.0.44:/home/liogen/workspace/timevortex/timevortex.data/backup

LOG_BASE_FOLDER = "LOG_BASE_FOLDER"
LOG_BASE_FOLDER_DEFAULT = "/tmp/timevortex"
SETTINGS_FILE_STORAGE_FOLDER = "SETTINGS_FILE_STORAGE_FOLDER"
SETTINGS_FILE_STORAGE_FOLDER_DEFAULT = "/tmp/data"


class Command(AbstractCommand):
    """Command class
    """

    help = MAIN_HELP_TEXT
    name = "backup command"
    logger = LOGGER
    sleep_time = 600

    def run(self, *args, **options):
        backup_target_path = get_backup_target_folder()
        if backup_target_path is None:
            self.logger.info(ERROR_TIMEVORTEX[ERROR_BACKUP_DEACTIVATED])
            return
        data_folder_path = getattr(settings, SETTINGS_FILE_STORAGE_FOLDER, SETTINGS_FILE_STORAGE_FOLDER_DEFAULT)
        log_folder_path = getattr(settings, LOG_BASE_FOLDER, LOG_BASE_FOLDER_DEFAULT)
        data_command = "rsync -azr %s %s" % (data_folder_path, backup_target_path)
        log_command = "rsync -azr %s %s" % (log_folder_path, backup_target_path)
        call_and_exit(data_command)
        call_and_exit(log_command)
