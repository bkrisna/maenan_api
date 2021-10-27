#!/usr/local/bin/python3
#########################################################################
# PURPOSE: main program body, to call diarium api                       #
# As this is a custom script, use it with your own risk.                #
# Any issue or difficulty, feel free to contact me.                     #
# @2021 - bkrisna - b.krisnamurti@gmail.com                             #
#########################################################################

import datetime
import json
from utils import logger
from d_api import *

def main():
    date = datetime.datetime.now();
    datestr = date.strftime("%Y-%m-%d")
    
    emp_data = {
        'emp_name': 'Bayu Krisnamurti',
        'emp_nik': '876594',
        'emp_pass': 'Welcome.4.09',
        'emp_lat' : '-6.424483627092651',
        'emp_lon' : '106.81285631028804',
    }

    logger ('D-API-TOK', True, "Get Diarium OAUTH API Token for: {emp_name}/{emp_nik}".format(emp_name=emp_data['emp_name'], emp_nik=emp_data['emp_nik']))
    oauth_tok = getOauthToken(emp_data['emp_nik'],emp_data['emp_pass'], "diarium_732870594", "XcvczE3TdXQP")
    logger ('D-API-TOK', True if oauth_tok else False, "OAUTH API Token: {token}".format(token=oauth_tok) if oauth_tok else "Failed to get OAUTH API Token")
    

    logger ('APIGW-TOK', True, "Get API GW Token for: {emp_name}/{emp_nik}".format(emp_name=emp_data['emp_name'], emp_nik=emp_data['emp_nik']))
    apigw_tok = getApigwToken("usrConsume", "consume**api123")
    if apigw_tok:
        logger ('APIGW-TOK', True, "API GW Token: {token}".format(token=apigw_tok))
    else:
        logger ('APIGW-TOK', False, "Failed to get GW API Token")
    
    logger ('CHECKIN', True, "Execute Checkin for: {emp_name}/{emp_nik}".format(emp_name=emp_data['emp_name'], emp_nik=emp_data['emp_nik']))
    doChek = checkIn(emp_data['emp_lat'], emp_data['emp_lon'], apigw_tok, oauth_tok)
    if doChek:
        logger ('CHECKIN', True, "Check in succesfull for: {emp_name}/{emp_nik}".format(emp_name=emp_data['emp_name'], emp_nik=emp_data['emp_nik']))
    else:
       logger ('CHECKIN', False, "Failed to do checkin for: {emp_name}/{emp_nik}".format(emp_name=emp_data['emp_name'], emp_nik=emp_data['emp_nik']))

    cinout_state = getCheckinStatus(oauth_tok)
    logger ('INOUT-ST', True, "Status Check In: {cin_state}; Status Check Out: {cout_state}".format(cin_state=cinout_state.get('has_checked_in'), cout_state=cinout_state.get('has_checked_out')))
    
# just calls the `main` function above
if __name__ == '__main__':
    main()