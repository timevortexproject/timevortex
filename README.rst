# Setup

* mkdir timevortex_v2
* mkvirtualenv timevortex_v2 --python=/usr/bin/python3
* sudo apt-get install python3 python3-dev

# Install

## Prod
    * pip install django requests python-dateutil pytz django-admin-tools psutil pyserial==2.5

## Dev
    * sudo apt-get install socat
    * pip install flake8 pylint django_nose behave_django pylint-django coverage prospector
    * [BLOCKED] pip install clonedigger django-fluent-dashboard django-admin-tools-stats

# Create application

* django-admin startproject timevortex
* python manage.py startapp weather
* python manage.py startapp hardware
* python manage.py startapp energy
* python manage.py startapp stubs
* python manage.py makemigrations weather
* python manage.py migrate
* python manage.py collectstatic


## TimeVortex backlog

* [BLOCKED]
    * [BLOCKED] Install and setup clonedigger (not python 3 compatible. Work in progress)
    * [BLOCKED] django-admin-tools-stats is not python 3 compatible

* Documentation
    * Update documentation for this project
    * Generate documentation from code
    * Generate document from .rst file

* CSV crawler
    * Finance     (CSV)
    * Garmin data (CSV)
    * Fitbit      (API) => http://python-fitbit.readthedocs.org/en/latest
    * Withing     (API) => https://github.com/maximebf/python-withings
    * Jawbone     (API) => http://kiefer.readthedocs.org/en/latest
    * Runkeeper   (API) 

* Hardware
    * Retrieve CPU data
    * Retrieve Memory data
    * Retrieve HDD data

## Timevortex idea

* Global
    * Split command into several celery job
    * Refactor metear script to include celery script to crawl the page and collect data. Then create a json element with "siteID", "variableID", "values" = [(value, date, dsttimezone, nondsttimezone)] that send 48 values to TSL with only one message. Store it into a CSV file and into DB. This should improve time to retrieve data and improve performance. Wait to install performance tracking before improving this script.
    * Use petl to manipulateur data.
    * Create à fonction that take into paramètres à matrix of variable and date and insert easily data in DB and send message over the network. 
        |       |  var1  | var2   |
        | time1 | value1 | value2 |
        | time2 | value3 | value4 |
    * Use vagrant David config
