#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import requests
import logging
import time
import httpx
import sys

# from wappdriver import WhatsApp

# Setting up log files
logging.basicConfig(filename='requests.log', level=logging.DEBUG,
                    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# Setting Up Proxies
proxies = 'http://127.0.0.1:8080'
slackURL = ''  # add slack webhook
cowinURL = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict'


# cowinURL=''

def message_slack(msg):
    msg = str(msg)
    try:
        requests.post(slackURL, data='{"text":"' + msg + '"}', verify=False, timeout=2)
    except requests.exceptions.RequestException as e:
        logging.error('Slack reachablility issue : ' + str(e))
        print('No Slacking:-->\t' + msg)
        return


def find_vaccine(query, headers):
    while True:
        try:
            with httpx.Client(http2=True, verify=False, proxies=proxies, timeout=10.0) as client:
                response = client.get(cowinURL, params=query, headers=headers)
                logging.info('Response time : ' + str(response.elapsed.total_seconds()))
                # print(response.http_version)
                # print('\x1b[1;32;40m' + ' Mission Hunt Response time : ' + str(response.elapsed.total_seconds()) + '\x1b[0m', end='\r', flush=True)
                availability = response.json()
                print('*********************************** ++++++++ ********************')
                print(type(availability))
                centers = availability['centers']
                for key in centers:
                    msg = ''
                    msg = 'Name: `' + key['name'] + '` Address: `' + key['address'] + '` Fees: *' + key['fee_type']
                    for capacity in key['sessions']:
                        if capacity['available_capacity'] > 0:
                            msg = msg + '* Vaccine Brand: ' + str(capacity['vaccine']) + ' For Age: `' + str(capacity['min_age_limit']) + '` Available : `' + str(capacity['available_capacity']) + '` *On Date* ' + str(capacity['date'])
                            message_slack(msg)
                            break
                    print('\n\n\n\n *************************')
                time.sleep(5)  # default Sleep for 10 Sec
        except requests.exceptions.RequestException as e:
            logging.error('Unable to reach Cowin Gateway ' + str(e))

def main():
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
    # pincode = input('\nEnter Pincode: ')

    # setup parameters
    query = {'district_id': '363', 'date': '15-05-2021'}

    availablity = find_vaccine(query, headers)
    message_slack(availablity)


if __name__ == '__main__':
    main()
