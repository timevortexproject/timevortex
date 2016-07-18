#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""Main client manage file for TimeVortex"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from timevortex.utils.globals import call_and_exit

# Globals
KEY_COMMAND = "command"
KEY_HELP_TEXT = "help_text"
MAIN_HELP_TEXT = "Invoke specific command relative to timevortex"
HELP_MESSAGE_COMMIT = "Commit your change and update changelog"
HELP_MESSAGE_RELEASE = "Create a new release"
# Options
OPTION_PREPARE = "prepare"
OPTION_LINT = "lint"
OPTION_QA = "qa"
OPTION_VALIDATE = "validate"
OPTION_BEHAVE = "behave"
OPTION_BEHAVE_ALL = "behave-all"
KEY_COMMIT = "commit"
KEY_RELEASE = "release"
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
        KEY_COMMAND: [
            "python manage.py migrate && "\
            "coverage run --source='.' manage.py behave --tags=wip --no-skipped && "\
            "coverage report -m"
        ],
        KEY_HELP_TEXT: "Launch behave test and coverage"
    },
    OPTION_BEHAVE_ALL: {
        KEY_COMMAND: ["python manage.py migrate && coverage run --source='.' manage.py behave && coverage report -m"],
        KEY_HELP_TEXT: "Launch all behave test and coverage"
    },
}

KEY_CURRENT = "current"
FILENAME_CHANGELOG = "CHANGELOG.rst"
PROJECT_NAME = "TimeVortex"
AUTHOR_NAME = "Pierre Leray"
AUTHOR_EMAIL = "pierreleray64@gmail.com"


def get_current_tag_version():
    """Return git tag version"""
    filename = "tmp.txt"
    cmd = "git describe --tags `git rev-list --tags --max-count=1` > %s"
    sh(cmd % filename)
    fil = open(filename)
    tag_version = fil.readlines()
    fil.close()
    sh("rm %s" % filename)
    tag_version = tag_version[0].replace("\n", "")
    return  tag_version.replace("v", "").split(".")


def update_changelog(message, version=KEY_CURRENT):
    """Add line into changelog"""
    changelog = open(FILENAME_CHANGELOG, "r")
    text = changelog.read().split("\n")
    changelog.close()
    changelog = open(FILENAME_CHANGELOG, "w")
    if version == KEY_CURRENT:
        text.insert(2, "* %s" % message)
    else:
        day = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        new_release = "%s (%s) stable; urgency=low\n\n" % (PROJECT_NAME, version)
        new_release += "* %s\n\n" % message
        new_release += "%s <%s>  %s\n" % (AUTHOR_NAME, AUTHOR_EMAIL, day)
        text = [new_release] + text
    changelog.write("\n".join(text))
    changelog.close()


def commit(message):
    """Commit using git"""
    update_changelog(message)
    call_and_exit("git add . && git commit -a -m '%s'" % message)
    call_and_exit("git push origin develop")


def release():
    """Release a new version"""
    current_version = get_current_tag_version()
    print(current_version)


class Command(BaseCommand):
    """Command class
    """

    help = MAIN_HELP_TEXT

    def add_arguments(self, parser):
        for argument in ARGUMENTS:
            parser.add_argument(
                "--%s" % argument,
                action="store_true",
                dest=argument,
                default=False,
                help=ARGUMENTS[argument][KEY_HELP_TEXT])
        parser.add_argument("--%s" % KEY_COMMIT, action="store", dest=KEY_COMMIT, help=HELP_MESSAGE_COMMIT)
        parser.add_argument("--%s" % KEY_RELEASE, action="store", dest=KEY_RELEASE, help=HELP_MESSAGE_RELEASE)


    def handle(self, *args, **options):
        if options[OPTION_VALIDATE]:
            options[OPTION_LINT] = True
            options[OPTION_BEHAVE_ALL] = True
            options[OPTION_QA] = True

        for command in ARGUMENTS:
            if options[command]:
                call_and_exit(ARGUMENTS[command][KEY_COMMAND])

        if KEY_COMMIT in options and options[KEY_COMMIT] is not None:
            commit(options[KEY_COMMIT])

        if KEY_RELEASE in options and options[KEY_RELEASE] is not None:
            commit(options[KEY_RELEASE])
