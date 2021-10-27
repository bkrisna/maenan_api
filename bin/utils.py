#!/usr/local/bin/python3
#########################################################################
# PURPOSE: common utils                                                 #
# As this is a custom script, use it with your own risk.                #
# Any issue or difficulty, feel free to contact me.                     #
# @2021 - bkrisna - b.krisnamurti@gmail.com                             #
#########################################################################

import base64
from urllib.parse import urlencode
import requests
import datetime

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def logger(ops, res, data):
    date = datetime.datetime.now();
    datestr = date.strftime("%Y/%m/%d %H:%M:%S")
    state = "success" if res else "failed"
    log = '[{0:s}][{1:^9s}][{2:^9s}][{3:s}]'.format(datestr, ops, state, data)
    print (log)
    return True

def get64(str):
    str_bytes = str.encode('ascii')
    b64_bytes = base64.b64encode(str_bytes)
    return b64_bytes.decode('ascii') 

def post_req( url, headers, data ):
    ses = requests.Session()
    ses.verify = False #disables SSL certificate verification

    try:
        res = ses.post(url, headers=headers, data=data)
        return res.json()
    except Exception as e:
        return str(e)

def get_req( url, headers ):
    ses = requests.Session()
    ses.verify = False #disables SSL certificate verification

    try:
        res = ses.get(url, headers=headers)
        return res.json()
    except Exception as e:
        return str(e)

def prep_url(baseUrl, act, urlParams=None):
    if urlParams is not None:
        return "{baseUrl}{act}?{qstring}".format(baseUrl=baseUrl, act=act, qstring=urlencode(urlParams, safe='+'))
    else:
        return "{baseUrl}{act}".format(baseUrl=baseUrl, act=act)