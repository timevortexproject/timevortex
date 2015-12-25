# Setup

* mkdir timevortex_v2
* mkvirtualenv timevortex_v2 --python=/usr/bin/python3

# Install

* pip install django requests
* pip install flake8 pylint django_nose behave_django pylint-django coverage
* [BLOCKED] pip install clonedigger

# Create application

* django-admin startproject timevortex
* python manage.py startapp weather
* python manage.py startapp stubs
* python manage.py makemigrations weather
* python manage.py sqlmigrate weather 0001
* python manage.py migrate

# Todo

## Weather application

* Create stubs to test this command
    * At least 2 differents airports
    * Historical data
    * New data
    * Doublon
    * Wrong data for each variable
* Create automatic testing for this command
    * Test different airport data retrieving
    * Test historical data retrieving
    * Test new data retrieving
    * Test no doublon data (statistics or not taken into account methods)
    * Test data send through RBMQ
    * Test storage of new value into files using timeserieslogger
    * Test wrong url
    * Test wrong content
    * Test down web service
    * Test wrong script parameter

## TimeVortex

* Code quality
    * [BLOCKED] Install and setup clonedigger (not python 3 compatible. Work in progress)

* Admin
    * Install django-extension
    * Install django-toolbar
    * Install django-admin-tools