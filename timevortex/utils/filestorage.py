#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""File storage adapter for timevortex project"""

import pytz
import dateutil.parser
from time import tzname
from datetime import datetime
from os import listdir, makedirs
from os.path import isfile, join, exists
from django.utils import timezone
from django.conf import settings
from timevortex.utils.globals import LOGGER, KEY_ERROR, KEY_SITE_ID, KEY_VARIABLE_ID, KEY_VALUE, KEY_DATE
from timevortex.utils.globals import KEY_DST_TIMEZONE, KEY_NON_DST_TIMEZONE, SYSTEM_SITE_ID

SETTINGS_FILE_STORAGE_FOLDER = "SETTINGS_FILE_STORAGE_FOLDER"
SETTINGS_DEFAULT_FILE_STORAGE_FOLDER = "/tmp/data/"


class FileStorage(object):
    """Class that help us to store and load data over several file"""

    def __init__(self, folder_path):
        """Constructor"""
        self.folder_path = folder_path

    def insert_series(self, series):
        """Insert series in DB

            :param series: Representation of a series
            :type series: dict.
        """
        self.insert(series)

    def insert(self, message):
        """Insert data in file"""
        file_folder = "%s/%s" % (self.folder_path, message[KEY_SITE_ID])
        file_date = timezone.localtime(
            dateutil.parser.parse(message[KEY_DATE]).replace(tzinfo=pytz.UTC)).strftime("%Y-%m-%d")

        if not exists(self.folder_path):
            makedirs(self.folder_path)

        if not exists(file_folder):
            makedirs(file_folder)

        raw_file = "%s/%s.tsv.%s" % (
            file_folder, message[KEY_VARIABLE_ID], file_date)
        extracted = open(raw_file, "a+")
        extracted.write("%s\t%s\t%s\t%s\n" % (
            message[KEY_VALUE],
            message[KEY_DATE],
            message[KEY_DST_TIMEZONE],
            message[KEY_NON_DST_TIMEZONE]))
        extracted.close()

    def insert_error(self, message):
        """Function that store error in errors collection and in log

            :param message: Error to insert in DB
            :type message: str.
        """
        LOGGER.error(message)
        message[KEY_VARIABLE_ID] = KEY_ERROR
        self.insert(message)

    def store_error(self, error):
        """Function that create valid error message

            :param error: Mal formed message
            :type error: str.
        """
        message = {
            KEY_VALUE: error,
            KEY_VARIABLE_ID: KEY_ERROR,
            KEY_SITE_ID: SYSTEM_SITE_ID,
            KEY_DATE: datetime.utcnow().isoformat('T'),
            KEY_DST_TIMEZONE: tzname[1],
            KEY_NON_DST_TIMEZONE: tzname[0]
        }
        LOGGER.error(error)
        self.insert(message)

    def get_series(self, site_id, variable_id):
        """Retrieve all series for a variable_id in site_id
        """
        element = variable_id
        file_prefix = "%s.tsv." % element
        site_folder = "%s/%s" % (self.folder_path, site_id)
        series = {}
        if exists(site_folder):
            for filename in listdir(site_folder):
                is_file = isfile(join(site_folder, filename))
                if is_file and file_prefix in filename:
                    completete_filename = "%s/%s" % (site_folder, filename)
                    temp_series = []
                    with open(completete_filename, "r") as f:
                        temp_series = f.readlines()
                        for line in temp_series:
                            array_line = line.split("\t")
                            if len(array_line) >= 2:
                                series[array_line[1]] = array_line[0]
        return series

    def get_last_series(self, site_id, variable_id):
        """Retrieve last value of variable_id in site_id
        """
        element = variable_id
        file_prefix = "%s.tsv." % element
        site_folder = "%s/%s" % (self.folder_path, site_id)
        if exists(site_folder):
            old_date = ""
            last_filename = ""
            for filename in listdir(site_folder):
                is_file = isfile(join(site_folder, filename))
                if is_file and file_prefix in filename:
                    date = filename.replace(file_prefix, "")
                    try:
                        date = datetime.strptime(date, "%Y-%m-%d")
                        if (old_date == "" or date > old_date):
                            old_date = date
                            last_filename = filename
                    except ValueError:
                        LOGGER.error("Not right file")

            last_filename = "%s/%s" % (site_folder, last_filename)
            with open(last_filename, "rb") as f:
                for last in f:
                    pass

            LOGGER.debug(last)
            last = last.decode("utf-8").replace("\n", "")

            return {
                KEY_VARIABLE_ID: element,
                KEY_SITE_ID: site_id,
                KEY_VALUE: last.split("\t")[0],
                KEY_DATE: last.split("\t")[1],
                KEY_DST_TIMEZONE: last.split("\t")[2],
                KEY_NON_DST_TIMEZONE: last.split("\t")[3]
            }

        return None

    def get_last_error(self, site_id):
        """Retrieve last error of a site_id file storage
        """
        return self.get_last_series(site_id, KEY_ERROR)

    def get_number_of_error(self, site_id, day_date):
        """This method retrieve number of error published for a day_date
        """
        element = KEY_ERROR
        site_folder = "%s/%s" % (self.folder_path, site_id)
        filename = "%s.tsv.%s" % (element, day_date)
        file_path = "%s/%s" % (site_folder, filename)
        if exists(site_folder) and exists(file_path):
            return sum(1 for line in open(file_path))
        return 0

    def get_number_of_series(self, site_id, day_date):
        """This method retrieve number of series published for a day_date
        """
        site_folder = "%s/%s" % (self.folder_path, site_id)
        series = {}

        if exists(site_folder):
            for filename in listdir(site_folder):
                if "%s.tsv" % KEY_ERROR not in filename and day_date in filename:
                    file_path = "%s/%s" % (site_folder, filename)
                    var_id = filename.replace(".tsv.%s" % day_date, "")
                    series_numbers = sum(1 for line in open(file_path))
                    series[var_id] = {KEY_VALUE: series_numbers}

        return series

    def set_data_location(self, folder_path):
        """Set data folder space"""
        self.folder_path = folder_path

FILE_STORAGE_SPACE = FileStorage(getattr(settings, SETTINGS_FILE_STORAGE_FOLDER, SETTINGS_DEFAULT_FILE_STORAGE_FOLDER))
