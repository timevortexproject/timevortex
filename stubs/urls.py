#!/usr/bin/python3
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

"""File that define Stubs urls"""

from django.conf.urls import url
from stubs.views import change_route_configuration, retrieve_metear_data, retrieve_bad_metear_data
from stubs.views import retrieve_metear_new_data


urlpatterns = [
    url(r'^change_route_configuration/?$', change_route_configuration, name='change_route_configuration'),
    url(
        r'^history/airport/(?P<airport>.*)/(?P<year>.*)/(?P<month>.*)/(?P<day>.*)/DailyHistory.html?$',
        retrieve_metear_data,
        name='retrieve_metear_data',
    ),
    url(
        r'^history/airport/(?P<airport>.*)/(?P<year>.*)/(?P<month>.*)/(?P<day>.*)/badcontent.html?$',
        retrieve_bad_metear_data,
        name='retrieve_bad_content_metear_data',
    ),
    url(
        r'^history/airport/(?P<airport>.*)/(?P<year>.*)/(?P<month>.*)/(?P<day>.*)/NewDailyHistory.html?$',
        retrieve_metear_new_data,
        name='retrieve_metear_new_data',
    ),
]
