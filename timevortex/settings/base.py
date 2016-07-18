#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-
"""
Django settings for timevortex project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5*0plcw(k&ywj+=d#@b6l%vx*b46z#n)07_om=do6!4xg*in25'  # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # 'fluent_dashboard',
    # 'admin_tools',
    # 'admin_tools.theming',
    # 'admin_tools.menu',
    # 'admin_tools.dashboard',
    # 'admin_tools_stats',
    # 'django_nvd3',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'djangobower',
    'django_nose',
    'behave_django',
    'stubs',
    'timevortex',
    'weather',
    'hardware',
    'energy',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'timevortex.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'timevortex', 'templates'),
        ],
        # 'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                # 'admin_tools.template_loaders.Loader',
            ]
        },
    },
]

WSGI_APPLICATION = 'timevortex.wsgi.application'

# Use nose to run all tests
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Tell nose to measure coverage on the 'foo' and 'bar' apps
NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=timevortex,weather,energy,hardware',
    '--exclude-dir=features/',
]

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'CET'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    # 'djangobower.finders.BowerFinder',
)

# BOWER_INSTALLED_APPS = (
#     'jquery#2.0.3',
#     'jquery-ui#~1.10.3',
#     'd3#3.3.6',
#     'nvd3#1.1.12-beta',
# )

#####
# LOGGING
#
LOG_BASE_FOLDER = "/var/log/timevortex"
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            "format": "%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': '%s/timevortex.log' % LOG_BASE_FOLDER,
            'when': 'd',
            'backupCount': 0,
            'formatter': 'verbose'
        },
        'file_weather': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': '%s/timevortex_weather.log' % LOG_BASE_FOLDER,
            'when': 'd',
            'backupCount': 0,
            'formatter': 'verbose'
        },
        'file_energy': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': '%s/timevortex_energy.log' % LOG_BASE_FOLDER,
            'when': 'd',
            'backupCount': 0,
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'timevortex': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'weather': {
            'handlers': ['file_weather'],
            'level': 'INFO',
            'propagate': True,
        },
        'energy': {
            'handlers': ['file_energy'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}


#####
# ADMIN CONFIGURATION
#

# ADMIN_TOOLS_INDEX_DASHBOARD = 'timevortex.dashboard.CustomIndexDashboard'
# ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'timevortex.dashboard.CustomAppIndexDashboard'
# ADMIN_TOOLS_INDEX_DASHBOARD = 'fluent_dashboard.dashboard.FluentIndexDashboard'
# ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'fluent_dashboard.dashboard.FluentAppIndexDashboard'
# ADMIN_TOOLS_MENU = 'fluent_dashboard.menu.FluentMenu'

#####
# TIMEVORTEX CONFIGURATION
#

SETTINGS_FILE_STORAGE_FOLDER = "/opt/timevortex/data"
SITE_URL = "http://127.0.0.1:8000"

#####
# WEATHER CONFIGURATION
#

METEAR_URL = "http://www.wunderground.com/history/airport/%s/%s/DailyHistory.html?format=1"
SETTINGS_METEAR_START_DATE = "2010-01-01"

#####
# BACKUP CONFIGURATION
#

BACKUP_TARGET_FOLDER = ""
