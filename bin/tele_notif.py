#!/usr/bin/python3
#########################################################################
# PURPOSE: notification to telegram bot                                 #
# As this is a custom script, use it with your own risk.                #
# Any issue or difficulty, feel free to contact me.                     #
# @2021 - bkrisna - b.krisnamurti@gmail.com                             #
#########################################################################

import requests


def put_tele_notif(token_id, chat_id, msg):
    #token_id = '1948644296:AAGlcpicAkhZsduhSOBxzEUlCKFF4T---yA'
    #chat_id = '-395089435'
    payload = {
        'chat_id': chat_id,
        'text': msg,
        'parse_mode': 'HTML'
    }
    return requests.post("https://api.telegram.org/bot{token}/sendMessage".format(token=token_id), data=payload).content