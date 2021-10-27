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

    logger ('APIFC-TOK', True, "Get Diarium OAUTH API Token for: {emp_name}/{emp_nik}".format(emp_name=emp_data['emp_name'], emp_nik=emp_data['emp_nik']))
    oauth_tok = getOauthToken(emp_data['emp_nik'],emp_data['emp_pass'], "diarium_732870594", "XcvczE3TdXQP")
    logger ('APIFC-TOK', True if oauth_tok else False, "Get OAUTH API Token {state}".format(state=("successfull" if oauth_tok else "failed")))
    

    logger ('APIGW-TOK', True, "Get API GW Token for: {emp_name}/{emp_nik}".format(emp_name=emp_data['emp_name'], emp_nik=emp_data['emp_nik']))
    apigw_tok = getApigwToken("usrConsume", "consume**api123")
    logger ('APIGW-TOK', True if apigw_tok else False, "Get API-GW Token {state}".format(state=("successfull" if apigw_tok else "failed")))
    
    logger ('CHECKOUT', True, "Execute Check Out for: {emp_name}/{emp_nik}".format(emp_name=emp_data['emp_name'], emp_nik=emp_data['emp_nik']))
    doChekOut = checkOut(emp_data['emp_lat'], emp_data['emp_lon'], apigw_tok, oauth_tok)
    logger ('CHECKOUT', True if doChekOut else False, "Check out {state} for: {emp_name}/{emp_nik}".format(emp_name=emp_data['emp_name'], emp_nik=emp_data['emp_nik'], state=("successfull" if doChekOut else "failed")))
    
    cinout_state = getCheckinStatus(oauth_tok)
    logger ('INOUT-ST', True, "Status Check In: {cin_state}; Status Check Out: {cout_state}".format(cin_state=cinout_state.get('has_checked_in'), cout_state=cinout_state.get('has_checked_out')))
    
# just calls the `main` function above
if __name__ == '__main__':
    main()