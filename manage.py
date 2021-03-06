#!/usr/bin/python3
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""Main module of django"""

import os
import sys


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "timevortex.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
