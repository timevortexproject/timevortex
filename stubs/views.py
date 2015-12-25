#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

import json
from django.views.decorators.http import require_POST, require_GET
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from stubs.models import StubsAPIOpening
from stubs.utils.globals import KEY_STUBS_OPEN_METEAR_API


@require_POST
@csrf_exempt
def change_route_configuration(request):
    # curl -i -H "Content-Type: application/json" -XPOST 'http://127.0.0.1:8000/stubs/change_route_configuration'
    # -d'{"open_metear_api": false}' && printf "\n"
    body = json.loads(request.body.decode('ascii'))
    open_metear_api = False
    if KEY_STUBS_OPEN_METEAR_API in body:
        open_metear_api = body[KEY_STUBS_OPEN_METEAR_API]

    try:
        api_route = StubsAPIOpening.objects.get(id=1)
        api_route.open_metear_api = open_metear_api
        api_route.save()
    except StubsAPIOpening.DoesNotExist:
        StubsAPIOpening.objects.create(
            open_metear_api=open_metear_api
        )
    data = {
        KEY_STUBS_OPEN_METEAR_API: open_metear_api,
    }
    return HttpResponse(json.dumps(data), content_type='application/json')


@require_GET
def retrieve_metear_data(request, airport, year, month, day):
    # curl -i -XGET 'http://127.0.0.1:8000/stubs/history/airport/LFMN/2015/12/23/DailyHistory.html' && printf "\n"
    try:
        api_route = StubsAPIOpening.objects.get(id=1)
    except StubsAPIOpening.DoesNotExist:
        return HttpResponseBadRequest()
    if api_route.open_metear_api is False:
        return HttpResponseBadRequest()
    html = "<html><head></head><body>%s</body></html>"
    csv = "\nHeureCET,TempératureC,Point de roséeC,Humidité,Pression au niveau de la merhPa,VisibilitéKm,Wind Direction,Vitesse du ventKm/h,"\
        "Vitesse des rafalesKm/h,Précipitationmm,Evénements,Conditions,WindDirDegrees,DateUTC\n"\
        "12:00 AM,12,6,59,1032,15,NNO,11.1,,,,Nuageux,2015-12-23 23:00:00\n"\
        "12:00 AM,13.0,7.0,67,1031,10.0,NNO,11.1,-,N/A,,Nuageux,2015-12-23 23:00:00\n"\
        "12:30 AM,12.0,6.0,67,1031,10.0,NO,14.8,-,N/A,,Nuageux,2015-12-23 23:30:00\n"\
        "1:00 AM,12,6,57,1032,15,NNO,16.7,,,,Nuageux,330,2015-12-24 00:00:00\n\n"
    all_html = html % csv
    return HttpResponse(all_html)
