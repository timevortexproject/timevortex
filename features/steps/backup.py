#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""Functionnal test for Backup"""

import shutil
import logging
from os.path import exists
from subprocess import call
from behave import given, when, then  # pylint: disable=E0611
from django.conf import settings
from timevortex.management.commands.backup import Command

BACKUP_TARGET_FOLDER = "BACKUP_TARGET_FOLDER"
BACKUP_TARGET_FOLDER_DEACTIVATE = None
BACKUP_TARGET_FOLDER_DEFAULT = "/tmp/backup"

BASE_FOLDER = "/tmp"
BACKUP_FOLDER = "/tmp/backup"
DATA_FOLDER_TEST1 = "data/test1"
DATA_FOLDER_TEST2 = "data/test2"
DATA_FOLDER_TEST1_FILE_1 = "data/test1/file1"
DATA_FOLDER_TEST1_FILE_2 = "data/test1/file2"
DATA_FOLDER_TEST2_FILE_3 = "data/test2/file3"
DATA_FOLDER_TEST1_FILE_4 = "data/test1/file4"
DATA_FOLDER_LOG_TV_LOG = "timevortex/tv.log"

LOGGER = logging.getLogger("timevortex")


def expected_file_and_data(backup=False, new_data=False):
    """Test of expected files and data"""
    assert exists("%s/%s" % (BASE_FOLDER, DATA_FOLDER_TEST1)) is True
    assert exists("%s/%s" % (BASE_FOLDER, DATA_FOLDER_TEST2)) is True
    assert exists("%s/%s" % (BASE_FOLDER, DATA_FOLDER_TEST1_FILE_1)) is True
    assert exists("%s/%s" % (BASE_FOLDER, DATA_FOLDER_TEST1_FILE_2)) is True
    assert exists("%s/%s" % (BASE_FOLDER, DATA_FOLDER_TEST2_FILE_3)) is True
    assert exists("%s/%s" % (BASE_FOLDER, DATA_FOLDER_LOG_TV_LOG)) is True

    assert exists("%s/%s" % (BACKUP_FOLDER, DATA_FOLDER_TEST1)) is backup
    assert exists("%s/%s" % (BACKUP_FOLDER, DATA_FOLDER_TEST2)) is backup
    assert exists("%s/%s" % (BACKUP_FOLDER, DATA_FOLDER_TEST1_FILE_1)) is backup
    assert exists("%s/%s" % (BACKUP_FOLDER, DATA_FOLDER_TEST1_FILE_2)) is backup
    assert exists("%s/%s" % (BACKUP_FOLDER, DATA_FOLDER_TEST2_FILE_3)) is backup
    assert exists("%s/%s" % (BACKUP_FOLDER, DATA_FOLDER_TEST1_FILE_4)) is new_data
    assert exists("%s/%s" % (BACKUP_FOLDER, DATA_FOLDER_LOG_TV_LOG)) is backup

    if backup:
        with open("%s/%s" % (BACKUP_FOLDER, DATA_FOLDER_TEST1_FILE_1), "r") as filed:
            content = filed.read()
            LOGGER.info("file contain : %s", content)
            if new_data:
                assert content == "12\n15\n"
            else:
                assert content == "12\n"


@given("I have data to backup")
def stubs_data_creation(context):
    """Data initialization"""
    # pylint: disable=unused-argument
    setattr(settings, BACKUP_TARGET_FOLDER, BACKUP_TARGET_FOLDER_DEFAULT)
    try:
        shutil.rmtree(BACKUP_FOLDER)
        shutil.rmtree("/tmp/data")
    except FileNotFoundError:
        pass
    call("mkdir /tmp/data", shell=True)
    call("mkdir %s/%s" % (BASE_FOLDER, DATA_FOLDER_TEST1), shell=True)
    call("mkdir %s/%s" % (BASE_FOLDER, DATA_FOLDER_TEST2), shell=True)
    call("touch %s/%s" % (BASE_FOLDER, DATA_FOLDER_TEST1_FILE_1), shell=True)
    call("touch %s/%s" % (BASE_FOLDER, DATA_FOLDER_TEST1_FILE_2), shell=True)
    call("touch %s/%s" % (BASE_FOLDER, DATA_FOLDER_TEST2_FILE_3), shell=True)
    call("touch %s/%s" % (BASE_FOLDER, DATA_FOLDER_LOG_TV_LOG), shell=True)
    call("echo '12' > %s/%s" % (BASE_FOLDER, DATA_FOLDER_TEST1_FILE_1), shell=True)
    call("echo '13' > %s/%s" % (BASE_FOLDER, DATA_FOLDER_TEST1_FILE_2), shell=True)
    call("echo '14' > %s/%s" % (BASE_FOLDER, DATA_FOLDER_TEST2_FILE_3), shell=True)
    call("echo 'log' > %s/%s" % (BASE_FOLDER, DATA_FOLDER_LOG_TV_LOG), shell=True)


@given("I add more data")
def stubs_new_data(context):
    """Write new data and validate that script retrieve it
    """
    # pylint: disable=unused-argument
    call("touch %s/%s" % (BASE_FOLDER, DATA_FOLDER_TEST1_FILE_4), shell=True)
    call("echo '15' >> %s/%s" % (BASE_FOLDER, DATA_FOLDER_TEST1_FILE_1), shell=True)
    call("echo '16' >> %s/%s" % (BASE_FOLDER, DATA_FOLDER_TEST1_FILE_2), shell=True)
    call("echo '17' >> %s/%s" % (BASE_FOLDER, DATA_FOLDER_TEST2_FILE_3), shell=True)
    call("echo '18' > %s/%s" % (BASE_FOLDER, DATA_FOLDER_TEST1_FILE_4), shell=True)


@given("I deactivate backup script")
def backup_script_deactivation(context):
    """Deactivate backup script"""
    # pylint: disable=unused-argument
    setattr(settings, BACKUP_TARGET_FOLDER, BACKUP_TARGET_FOLDER_DEACTIVATE)


@when("I run the backup command")
def run_backup_command(context):
    """Run backup command"""
    # pylint: disable=unused-argument
    command = Command()
    command.handle()


@then("nothing should be backuped")
def no_data_expected(context):
    """No data expected"""
    # pylint: disable=unused-argument
    expected_file_and_data(False, False)


@then("I should see backuped data")
def expected_data(context):
    """Expected data"""
    # pylint: disable=unused-argument
    expected_file_and_data(True, False)


@then("I should see new backuped data")
def expected_new_data(context):
    """Expected new data"""
    # pylint: disable=unused-argument
    expected_file_and_data(True, True)
