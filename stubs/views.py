#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-

import json
from django.views.decorators.http import require_POST, require_GET
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
# from timevortex.utils.globals import LOGGER
from stubs.models import StubsAPIOpening
from stubs.utils.globals import KEY_STUBS_OPEN_METEAR_API
from features.steps.test_utils import TEST_METEAR_SITE_ID_2, DICT_METEAR_FAKE_DATA, DICT_METEAR_FAKE_NEWS_DATA
from features.steps.test_utils import TEST_METEAR_SITE_ID, KEY_METEAR_FAKE_DATA_ELEMENTS, KEY_METEAR_FAKE_DATA_DATE


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


def is_metear_api_open():
    try:
        api_route = StubsAPIOpening.objects.get(id=1)
    except StubsAPIOpening.DoesNotExist:
        return False
    if api_route.open_metear_api is False:
        return False
    return True


def generate_metear_csv(fixtures, day):
    csv = "\nHeureCET,TempératureC,Point de roséeC,Humidité,Pression au niveau de la merhPa,VisibilitéKm,"\
        "Wind Direction,Vitesse du ventKm/h,Vitesse des rafalesKm/h,Précipitationmm,Evénements,Conditions,"\
        "WindDirDegrees,DateUTC<br />\n"
    for element in fixtures:
        data_day = element[KEY_METEAR_FAKE_DATA_DATE].split(" ")[0].split("-")[2]
        if day == data_day:
            csv += ",".join(element[KEY_METEAR_FAKE_DATA_ELEMENTS])
            csv += ",%s<br />\n" % element[KEY_METEAR_FAKE_DATA_DATE]
    csv += "\n"
    return csv


@require_GET
def retrieve_metear_new_data(request, airport, year, month, day):
    # curl -i -XGET 'http://127.0.0.1:8000/stubs/history/airport/LFMN/2015/12/23/DailyHistory.html' && printf "\n"
    if not is_metear_api_open():
        return HttpResponseBadRequest()
    csv = generate_metear_csv(DICT_METEAR_FAKE_NEWS_DATA, day)
    return HttpResponse(csv)


@require_GET
def retrieve_metear_data(request, airport, year, month, day):
    # curl -i -XGET 'http://127.0.0.1:8000/stubs/history/airport/LFMN/2015/12/23/DailyHistory.html' && printf "\n"
    if not is_metear_api_open():
        return HttpResponseBadRequest()
    csv = generate_metear_csv(DICT_METEAR_FAKE_DATA, day)
    return HttpResponse(csv)


@require_GET
def retrieve_bad_content_metear_data(request, airport, year, month, day):
    # curl -i -XGET 'http://127.0.0.1:8000/stubs/history/airport/LFMN/2015/12/23/badcontent.html' && printf "\n"
    if not is_metear_api_open():
        return HttpResponseBadRequest()
    html = "<html><head></head><body>%s</body></html>"
    if airport in TEST_METEAR_SITE_ID:
        csv = "snqfzfzfz,fs,dmlkmùqkfml,mkef,mkzenfzmlk,mlr,mzl,ml,zfml,fmlez,ml"
    elif airport in TEST_METEAR_SITE_ID_2:
        csv = "<br />\n<br />\n<br />snq,,,,,,,,,,fzfzfz,fs,dmlkmùqkfml,mkef,mkzmlk,mlr,mzl,ml,zfml,fmlez,ml<br />\n"
    all_html = html % csv
    return HttpResponse(all_html)
