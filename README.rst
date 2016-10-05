.. image:: https://travis-ci.org/timevortexproject/timevortex.svg?branch=develop
    :target: https://travis-ci.org/timevortexproject/timevortex

.. image:: https://coveralls.io/repos/github/timevortexproject/timevortex/badge.svg?branch=develop
    :target: https://coveralls.io/github/timevortexproject/timevortex?branch=develop 

.. image:: https://codeclimate.com/github/timevortexproject/timevortex/badges/gpa.svg
    :target: https://codeclimate.com/github/timevortexproject/timevortex
    :alt: Code Climate

Setup
=====

* mkdir timevortex_v2
* mkvirtualenv timevortex_v2 --python=/usr/bin/python3
* sudo apt-get install python3 python3-dev

Install
=======

Prod
----

* sudo apt-get install python3 python3-dev sqlite3
* pip install django requests python-dateutil pytz django-admin-tools psutil pyserial
* mkdir /var/log/timevortex

Dev
---
    
* sudo apt-get install socat git-flow
* pip install flake8 pylint django_nose behave_django pylint-django coverage prospector nose-exclude
* [BLOCKED] pip install clonedigger django-fluent-dashboard django-admin-tools-stats
* mkdir /tmp/timevortex

Create application
==================

* Create Django apps:
    * django-admin startproject timevortex
    * python manage.py startapp weather
    * python manage.py startapp hardware
    * python manage.py startapp energy
    * python manage.py startapp stubs
    * python manage.py makemigrations weather
    * python manage.py migrate
    * python manage.py collectstatic
    * python manage.py createsuperuser --settings=timevortex.settings.local
        * timevortex / timevortex_Admin
* Manage project
    * python manage.py timevortex --commit "Your commit message" --settings=timevortex.settings.local


Snap build
==========

* sudo apt-get install software-properties-common
* sudo add-apt-repository ppa:snappy-dev/tools
* sudo apt-get update
* sudo apt-get install snapcraft
* snapcraft init (create a yml file)
* snapcraft stage (retrieve source and install dependencies)
* snapcraft snap (build snap)
* snapcraft (build final snap package)
* sudo apt-get install snapd
* sudo snap install timevortex_2.0.1_amd64.snap --devmode --force-dangerous
* sudo snap try prime --devmode
* cp /vagrant/snapcraft.yaml . && cp /vagrant/timevortex-prepare . && snapcraft clean && snapcraft && sudo snap try prime --devmode

TimeVortex todo
===============

* CurrentCost:
    * Run script with snap
    * Test scritp with socat (bad port, good port bad message, correct message, correct message kwh increase)
* Prod :
    * Avoid update initial_data if useless (rewrite user properties)
    * Test daily-report
    * Test backup in USB key
    * Test currentcost live
    * Migrate data to new currentcost
    * Setup raspberry pi installation at home
    * Remove develop branch in snapcraft.yml
    * Put snap folder in timevortex folder

TimeVortex backlog
==================

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
* API
    * Fitbit      (API) => http://python-fitbit.readthedocs.org/en/latest
    * Withing     (API) => https://github.com/maximebf/python-withings
    * Jawbone     (API) => http://kiefer.readthedocs.org/en/latest
    * Runkeeper   (API) 

* Hardware
    * Retrieve CPU data
    * Retrieve Memory data
    * Retrieve HDD data

Timevortex idea
---------------

* Global
    * Split command into several celery job
    * Refactor metear script to include celery script to crawl the page and collect data. Then create a json element with "siteID", "variableID", "values" = [(value, date, dsttimezone, nondsttimezone)] that send 48 values to TSL with only one message. Store it into a CSV file and into DB. This should improve time to retrieve data and improve performance. Wait to install performance tracking before improving this script.
    * Use petl to manipulate data.
    * Create à fonction that take into paramètres à matrix of variable and date and insert easily data in DB and send message over the network. 
        |       |  var1  | var2   |
        | time1 | value1 | value2 |
        | time2 | value3 | value4 |
    * Use vagrant David config
* Technology
    * Microservice with python and django, microservice django
    * Docker, host docker image

* Idea:
    * Force user to register with gmail account. Use this gmail account to send email for daily report. Email account should be sender and receiver
    * Use google SSO to register a user and retrieve information about him
    * Define a flow to register and configure an account into timevortex paltform and create functional tests based on this flow
    * user should select a city where he actually leaves. City selection propose lang and unit that user want to use. By default lang is browser language, unit is metrics system

* UI:
    * Chart with aggregation to 3 months (temperature, kWh, split hp/hc)
    * Chart with aggreggation to 1 month (temperature, kWh, split hp/hc)
    * Chart per week
    * Chart per day

* Use cases:
    * CRUD user into platform
    * CRUD site information
    * CRUD sensor (adding a sensor create several variables. User is free to add or not a variable)
    * CRUD variables
    * Link variable to a room or to a site
    * Choose representation (timeline or site plan with top view and all variable all around)
    * Optional : A variable is the combination of several variable

* Adding a sensor :
    * Choice by brand and model
    * Define parameter for the sensor
    * List of generated variable

* Use django as plugin provider to reduce time to create a plugin and simplify deployment
* Each django app should create a django command that use RBMQ and define a REST API to retrieve data
* Create a Django app per thematics like weather, electricity, finance, health
* Create a Djnago stubs app for stubs that could be activated by settings

Consulting
-----------------
    * Être quelqu'un qui aide les gens à y voir plus clair dans leurs données
    * Proposer un système automatique de collecte et d'analyse de différents types de données
    * Proposer des simulations pour améliorer certains points
    * Faire la liste des points qui pourraient être améliorer
    * Proposer un blog autour des améliorations possibles
    * Proposer des jeux afin de se connaitre mieux
    * Ces jeux doivent être ouvert à tous sous excell par exemple
    * Apprendre en s'amusant pour attirer les gens
    * Ensuite rendre une solution packages pour automatiser tous ça
    * Ouvrir un blog sur le quantified self est essayé de le démocratiser



