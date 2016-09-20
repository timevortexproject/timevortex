#!/usr/bin/python3
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

""" Setup.py script """

import os
# from setuptools import find_packages, setup
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

PROJECT = "timevortex"

INSTALL_REQS = [
    "django==1.9.1",
    "requests",
    "python-dateutil",
    "pytz",
    "django-admin-tools",
    "pyserial",
]

VERSION = "2.1.2"

setup(
    name="%s" % (PROJECT),
    version=VERSION,
    description="Open source data logging platform for Internet of Things",
    long_description=open('README.rst').read(),
    author="Pierre Leray",
    author_email="pierreleray64@gmail.com",
    url="https://github.com/timevortexproject/%s" % (PROJECT),
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Operating System :: Unix",
        "Topic :: Home Automation",
        "License :: OSI Approved :: MIT License",
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.9',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    packages=["timevortex", "energy", "weather"],
    # scripts=["bin/%s" % (PROJECT)],
    install_requires=INSTALL_REQS,
    zip_safe=False,
    include_package_data=True,
    data_files=[
        ('', ['manage.py', 'timevortex/']),
    ],
    # data_files=[
    #     ('/opt/timevortex', [
    #         'logs/%s.conf' % (PROJECT),
    #         'config/config.ini']),
    #     ('/etc/supervisor/conf.d', [
    #         'supervisor/timevortex.currentcost.conf',
    #         'supervisor/timevortex.timeserieslogger.conf']),
    # ],
)
