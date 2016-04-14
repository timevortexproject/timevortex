#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""File storage adapter for timevortex project"""

import shutil
from os.path import exists
from django.conf import settings
from timevortex.utils.filestorage import SETTINGS_DEFAULT_FILE_STORAGE_FOLDER, SETTINGS_FILE_STORAGE_FOLDER
from features.steps.test_utils import TEST_CC_SITE_ID

STORAGE_SPACE = getattr(settings, SETTINGS_FILE_STORAGE_FOLDER, SETTINGS_DEFAULT_FILE_STORAGE_FOLDER)


def clean_folder():
    FOLDER_PATH = "%s/%s" % (STORAGE_SPACE, TEST_CC_SITE_ID)
    if exists(FOLDER_PATH):
        shutil.rmtree(FOLDER_PATH)
    FOLDER_PATH = "%s/%s" % (STORAGE_SPACE, "system")
    if exists(FOLDER_PATH):
        shutil.rmtree(FOLDER_PATH)