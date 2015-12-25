#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

from django.conf.urls import url
from stubs.views import change_route_configuration, retrieve_metear_data


urlpatterns = [
    url(r'^change_route_configuration/?$', change_route_configuration, name='change_route_configuration'),
    url(
        r'^history/airport/(?P<airport>.*)/(?P<year>.*)/(?P<month>.*)/(?P<day>.*)/DailyHistory.html?$',
        retrieve_metear_data,
        name='retrieve_metear_data',
    ),
]
