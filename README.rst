# Setup

* mkdir timevortex_v2
* mkvirtualenv timevortex_v2 --python=/usr/bin/python3

# Install

* pip install django requests python-dateutil pytz django-admin-tools
* pip install flake8 pylint django_nose behave_django pylint-django coverage
* [BLOCKED] pip install clonedigger

# Create application

* django-admin startproject timevortex
* python manage.py startapp weather
* python manage.py startapp stubs
* python manage.py makemigrations weather
* python manage.py migrate
* python manage.py collectstatic

# Todo

## Weather application

* Separate METEAR log in a specific file
* Add daily rotation for log

## TimeVortex

* Code quality
    * [BLOCKED] Install and setup clonedigger (not python 3 compatible. Work in progress)

* Admin
    * Install django-extension
    * Install django-toolbar
    * Install django-admin-tools
    * Install chrnograph to manage cron task
    * Migrate on postgresql DB
    * Modify settings.py to be production ready
    * Create a local.py that define development settings
    * Clean coverage report