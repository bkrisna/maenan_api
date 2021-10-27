#!/usr/local/bin/python3
#########################################################################
# PURPOSE: api call diarium                                             #
# As this is a custom script, use it with your own risk.                #
# Any issue or difficulty, feel free to contact me.                     #
# @2021 - bkrisna - b.krisnamurti@gmail.com                             #
#########################################################################

import base64
import json
from urllib.parse import urlencode
from utils import *

baseUrls = {
    'factoryBaseUrl' : "https://apifactory.telkom.co.id:8243/hcm/api/diarium",
    'gwBaseUrl' : "https://apigw.telkom.co.id:7777"
}

def getOauthToken(d_uname, d_passwd, api_uname, api_passwd):
    act = "/authorization/v1/oauth/token"
    url = prep_url(baseUrls['factoryBaseUrl'], act)
    payload = {
        'grant_type' : 'password',
        'username' : d_uname,
        'password' : d_passwd,
        'is_get' : 'true'
    }

    base64string = get64("{uname}:{passwd}".format(uname=api_uname, passwd=api_passwd))
    headers = {
        'X-Authorization': 'Basic {auth_string}'.format(auth_string=base64string),
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    try:
        res = post_req(url, headers, urlencode(payload))
        return res.get('access_token')
    except Exception as e:
        logger ("APIFC-TOK", False, str(e))
        return False

def getApigwToken(gw_uname, gw_passwd):
    act = "/rest/pub/apigateway/jwt/getJsonWebToken"
    urlParams = {
        'app_id' : 'cddc614d-9edb-430b-a1d9-783adc2a42c2'
    }
    url = prep_url(baseUrls['gwBaseUrl'], act, urlParams)
    base64string = get64("{uname}:{passwd}".format(uname=gw_uname, passwd=gw_passwd))

    headers = {
        'Authorization': 'Basic {auth_string}'.format(auth_string=base64string),
        'Accept': 'application/json',
    }

    try:
        res = get_req(url, headers)
        return res.get('jwt')
    except Exception as e:
        logger ("APIGW-TOK", False, str(e))
        return False


def getCheckinStatus(api_token):
    act = "/time-management/v1/absensi"
    urlParams = {
        'action' : 'checkinout',
        'user_timezone' : "GMT+7",
        'app_version' : '4.4.2'
    }
    url = prep_url(baseUrls['factoryBaseUrl'], act, urlParams)
    headers = {
        'X-Authorization': "bearer {token}".format(token=api_token),
    }

    try:
        return get_req(url, headers).get('data')
    except Exception as e:
        logger ("INOUT-ST", False, str(e))
        return str(e)

def checkIn(usr_lat, usr_lon, gwToken, factoryToken):
    act = "/gateway/telkom-diarium-timemanagement/1.0/timeManagement/absensi/checkin"
    url = prep_url(baseUrls['gwBaseUrl'], act)
    payload = {
        "catatan_checkin": "absentmasuk",
        "feeling": "",
        "ip_address": "ip-null-v3.15.0",
        "kota": "Depok",
        "lang_checkin": usr_lat,
        "local_date_time": None,
        "long_checkin": usr_lon,
        "nik": None,
        "posisi": "Kartini, Depok, Jawa Barat, 16439, Indonesia",
        "question_answers": [
        {
            "question_choice_id": 8,
            "question_choice_text": "",
            "question_id": 3
        },
        {
            "question_choice_id": 10,
            "question_choice_text": "",
            "question_id": 1
        }
        ],
        "shift": "false",
        "timezone": "GMT+7",
        "versi": "4.4.2"
    }

    headers = {
        'X-Authorization': "bearer {ftoken}".format(ftoken=factoryToken),
        'Authorization': "bearer {gwtoken}".format(gwtoken=gwToken),
        'Content-Type': 'application/json'
    }

    try:
        return post_req(url, headers, payload)
    except Exception as e:
        logger ("CHECKIN", False, str(e))
        return False

def checkOut(usr_lat, usr_lon, gwToken, factoryToken):
    act = "/gateway/telkom-diarium-timemanagement/1.0/timeManagement/absensi/checkout"
    url = prep_url(baseUrls['gwBaseUrl'], act)
    payload = {
        "catatan_checkout": "absentpulang",
        "feeling": "",
        "ip_address": "ip-null-v3.15.0",
        "lang_checkout": usr_lat,
        "local_date_time": None,
        "long_checkout": usr_lon,
        "nik": None,
        "posisi": "-",
        "question_answers": [
            {
                "question_choice_id": 8,
                "question_choice_text": "",
                "question_id": 3
            },
            {
                "question_choice_id": 10,
                "question_choice_text": "",
                "question_id": 1
            }
        ],
        "timezone": "GMT+7"
    }

    headers = {
        'X-Authorization': "bearer {token}".format(token=factoryToken),
        'Authorization': "bearer {token}".format(token=gwToken),
        'Content-Type': 'application/json'
    }

    try:
        res = post_req(url, headers, payload)
        print (res)
        return True
    except Exception as e:
        logger ("CHECKOUT", False, str(e))
        return False