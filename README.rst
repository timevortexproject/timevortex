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
    * Test CMS integration into django app to manage content only through this option

* Documentation
    * Update documentation for this project

* Code quality
    * Clean coverage report
    * Pass pylint test
    * Integrate code into github
    * Integrate code with travis
    * Integrate a profiler for development

* Deployment
    * Simplify deployment
    * Migrate on postgresql DB
    * Modify settings.py to be production ready
    * Create a local.py that define development settings
    
* Admin
    * Install django-extension
    * Install django-toolbar
    * Install chronograph to manage cron task
    * Install sentry

* TimeVortex
    * Create an email that send daily report
    * Create a backup tools
        * cd /opt/timevortex/data/ && rsync -az liogen_home liogen@192.168.0.44:/home/liogen/workspace/timevortex/timevortex.data/backup
        * cd /var/log && rsync -az timevortex liogen@192.168.0.44:/home/liogen/workspace/timevortex/timevortex.data/backup
    * Add daily rotation for log
    * Create commit, release, changelog, ... tools
    * Clean laptop folder

* CurrentCost
    * Integrate currentcost module

* CSV crawler
    * Finance
    * Garmin data

* Hardware
    * Retrieve CPU data
    * Retrieve Memory data
    * Retrieve HDD data

## Timevortex idea

* Global
    * Split command into several celery job
    * Refactor metear script to include celery script to crawl the page and collect data. Then create a json element with "siteID", "variableID", "values" = [(value, date, dsttimezone, nondsttimezone)] that send 48 values to TSL with only one message. Store it into a CSV file and into DB. This should improve time to retrieve data and improve performance. Wait to install performance tracking before improving this script.
