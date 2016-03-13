# Setup

* mkdir timevortex_v2
* mkvirtualenv timevortex_v2 --python=/usr/bin/python3
* sudo apt-get install python3 python3-dev

# Install

## Prod
    * pip install django requests python-dateutil pytz django-admin-tools psutil pyserial==2.5

## Dev
    * sudo apt-get install socat
    * pip install flake8 pylint django_nose behave_django pylint-django coverage
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

* CMS
    * (1.5)  Test CMS integration into django app to manage content only through this option

* Documentation
    * Update documentation for this project
    * Generate documentation from code
    * Generate document from .rst file

* Code quality
    * (0.5)  Refactor behave test to organise metear stuff in metear.py, energy stuff in currentcost.py, common stuff in test_utils
    * (0.25) Clean coverage report
    * (0.5)  Pass pylint test
    * Integrate code into github
    * Integrate code with travis
    * Integrate a profiler for development

* Deployment
    * (5)    Simplify deployment (study approach + setup.py + pip install + debian package + docker)
    * (0.25) Migrate on postgresql
    * (0.25) Modify settings.py to be production ready + create a local.py that define development settings
    
* Admin
    * (0.25) Install django-extension + django-toolbar + sentry
    * (0.5)  Install chronograph to manage cron task

* TimeVortex
    * (0.5)  Create an email that send daily report
    * (1)    Create a backup tools
        * cd /opt/timevortex/data/ && rsync -az liogen_home liogen@192.168.0.44:/home/liogen/workspace/timevortex/timevortex.data/backup
        * cd /var/log && rsync -az timevortex liogen@192.168.0.44:/home/liogen/workspace/timevortex/timevortex.data/backup
    * (0.5)  Add daily rotation for log
    * (2)    Create commit, release, changelog, ... tools
    * (1)    Clean laptop folder
    * (0.5)  Avoid to access DB data from Sites.objects... or Variables.objects...

* CurrentCost
    * (1)    Integrate currentcost module

* CSV crawler
    * Finance (CSV)
    * Garmin data (CSV)
    * Fitbit (API)
    * Withing (API)
    * Jawbone (API)
    * Runkeeper (API)

* Hardware
    * Retrieve CPU data
    * Retrieve Memory data
    * Retrieve HDD data

## Timevortex idea

* Global
    * Split command into several celery job
    * Refactor metear script to include celery script to crawl the page and collect data. Then create a json element with "siteID", "variableID", "values" = [(value, date, dsttimezone, nondsttimezone)] that send 48 values to TSL with only one message. Store it into a CSV file and into DB. This should improve time to retrieve data and improve performance. Wait to install performance tracking before improving this script.
