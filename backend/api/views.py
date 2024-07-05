from rest_framework.response import Response
from rest_framework.request import Request
from django.http import HttpRequest
from rest_framework.decorators import api_view
import requests
import os
from pprint import pprint


def get_geodata(ip: str) -> dict[str]:
    API_KEY = os.environ.get("API_KEY")
    URL = "http://api.weatherapi.com/v1/ip.json?key={}&q={}".format(API_KEY, ip)

    response = requests.get(URL).json()

    continent = response["continent_name"]
    country = response["country_name"]
    city = response["city"]
    localtime = response["localtime"]
    region = response["region"]

    return {
        "continent": continent,
        "country": country,
        "city": city,
        "region": region,
        "localtime": localtime,
    }


def get_client_ip(request: HttpRequest):
    XFF: str = request.META.get("HTTP_X_FORWARDED_FOR")
    client_ip = ""

    if XFF:
        client_ip = XFF.split(",")[0]
    else:
        client_ip = request.META.get("REMOTE_ADDR")

    return client_ip


@api_view(["GET"])
def get_me(request: Request):
    # get client ip address
    client_ip = get_client_ip(request)

    # get client geodata
    geodata = get_geodata(client_ip)

    payload = {"client_ip": client_ip, "geodata": geodata}

    return Response(data=payload)
