#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import requests
import logging
import time
import httpx
import sys
import telegram_send
from datetime import date

# Setting up log files
logging.basicConfig(filename='requests.log', level=logging.INFO,
                    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

cowinURLdist = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict'
cowinURLPin = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin'


def message_telegram(msg):
    msg = str(msg)
    try:
        telegram_send.send(messages=[msg])
    except requests.exceptions.RequestException as e:
        logging.error('Telegram reachability issue : ' + str(e))
        print('No Telegram:-->\t' + msg)
        return


def find_vaccine(query, headers, cowinURL):
        try:
            with httpx.Client(http2=True, verify=False) as client:
                response = client.get(cowinURL, params=query, headers=headers)
                logging.info('Response time : ' + str(response.elapsed.total_seconds()))
                # print(response.http_version)
                print('\x1b[1;32;40m' + ' Mission Hunt Response time : ' + str(response.elapsed.total_seconds()) + '\x1b[0m', end='\r', flush=True)
                availability = response.json()
                print('*********************************** ++++++++ ********************')
                print(type(availability))
                centers = availability['centers']
                for key in centers:
                    print('******* '+key['name']+' ********')
                    msg = 'Name: <b>' + key['name'] + '</b> Address: ' + key['address'] + ' Fees: ' + key['fee_type']
                    for capacity in key['sessions']:
                        print(str(capacity['available_capacity'])+' on date '+str(capacity['date'])+'')
                        if capacity['available_capacity'] > 0 and capacity['min_age_limit'] < 45:
                            msg = msg + ' Vaccine Brand: ' + str(capacity['vaccine']) + ' For Age: ' + str(capacity['min_age_limit']) + ' Available : ' + str(capacity['available_capacity']) + ' *On Date* ' + str(capacity['date'])
                            logging.info(msg)
                            message_telegram(msg)
                            print(msg)
        except requests.exceptions.RequestException as e:
            logging.error('Unable to reach Cowin Gateway ' + str(e))
        #exit(0)


def main():
    today = date.today()
    search_date = today.strftime("%d-%m-%Y")
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': 'https://www.cowin.gov.in/',
        'Origin': 'https://www.cowin.gov.in',
        'Te': 'trailers',
        'Connection': 'close',
    }
    # setup parameters
    # Mumbai = 995
    # East Delhi = 145
    # Pune = 363
    query = {'district_id': '363', 'date': search_date}
    query2 = {'pincode': '110091', 'date': search_date}
    while True:
        find_vaccine(query, headers, cowinURLdist)
        find_vaccine(query2, headers, cowinURLPin)
        time.sleep(1800)  # default Sleep for 5 Min
    exit(0)

if __name__ == '__main__':
    main()
