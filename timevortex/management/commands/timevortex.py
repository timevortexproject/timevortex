#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""Main client manage file for TimeVortex"""

from subprocess import call
from django.core.management.base import BaseCommand

# Globals
KEY_COMMAND = "command"
KEY_HELP_TEXT = "help_text"
MAIN_HELP_TEXT = "Invoke specific command relative to timevortex"
# Options
OPTION_PREPARE = "prepare"
OPTION_LINT = "lint"
OPTION_QA = "qa"
OPTION_VALIDATE = "validate"
OPTION_BEHAVE = "behave"
OPTION_BEHAVE_ALL = "behave_all"
# Arguments
ARGUMENTS = {
    OPTION_LINT: {
        KEY_COMMAND: ["flake8"],
        KEY_HELP_TEXT: "Lint code using flake8 and configuration in setup.cfg",
    },
    OPTION_QA: {
        # KEY_COMMAND: ["pylint *.py */*.py */*/*.py */*/*/*.py -f html --rcfile=.pylintrc > qa.html"],
        KEY_COMMAND: ["prospector -F"],
        KEY_HELP_TEXT: "Validate qualilty of code using pylint and configuration .pylintrc",
    },
    OPTION_VALIDATE: {
        KEY_COMMAND: ["python manage.py test"],
        KEY_HELP_TEXT: "Validate code using lint, test and qa verification",
    },
    OPTION_PREPARE: {
        KEY_COMMAND: ["pip install flake8 pylint django_nose behave_django pylint-django coverage prospector"],
        KEY_HELP_TEXT: "Install dependencies for development mode"
    },
    OPTION_BEHAVE: {
        KEY_COMMAND: ["coverage run --source='.' manage.py behave --tags=wip --no-skipped && coverage report -m"],
        KEY_HELP_TEXT: "Launch behave test and coverage"
    },
    OPTION_BEHAVE_ALL: {
        KEY_COMMAND: ["coverage run --source='.' manage.py behave && coverage report -m"],
        KEY_HELP_TEXT: "Launch all behave test and coverage"
    },
}


def call_and_exit(command, shell=False):
    """Call a shell command and exit if error
    """
    code = call(command, shell=shell)
    if code != 0:
        exit(1)


class Command(BaseCommand):
    """Command class
    """

    help = MAIN_HELP_TEXT

    def add_arguments(self, parser):
        for argument in ARGUMENTS:
            parser.add_argument(
                '--%s' % argument,
                action='store_true',
                dest=argument,
                default=False,
                help=ARGUMENTS[argument][KEY_HELP_TEXT])

    def handle(self, *args, **options):
        if options[OPTION_LINT] or options[OPTION_VALIDATE]:
            call_and_exit(ARGUMENTS[OPTION_LINT][KEY_COMMAND])
        if options[OPTION_VALIDATE]:
            call_and_exit(ARGUMENTS[OPTION_VALIDATE][KEY_COMMAND], shell=True)
        if options[OPTION_BEHAVE]:
            call_and_exit(ARGUMENTS[OPTION_BEHAVE][KEY_COMMAND], shell=True)
        if options[OPTION_BEHAVE_ALL] or options[OPTION_VALIDATE]:
            call_and_exit(ARGUMENTS[OPTION_BEHAVE_ALL][KEY_COMMAND], shell=True)
        if options[OPTION_QA] or options[OPTION_VALIDATE]:
            call_and_exit(ARGUMENTS[OPTION_QA][KEY_COMMAND], shell=True)
        if options[OPTION_PREPARE]:
            call_and_exit(ARGUMENTS[OPTION_PREPARE][KEY_COMMAND], shell=True)
