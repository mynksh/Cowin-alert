#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import requests
import logging
import time
import httpx
import sys
#from wappdriver import WhatsApp

#Setting up log files
logging.basicConfig(filename='requests.log', level=logging.DEBUG, format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

#Setting Up Proxies
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}
slackURL='' # add slack webhook
cowinURL='https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict'
#cowinURL=''

def message_slack(msg):
    msg = str(msg)
    try:
        requests.post(slackURL,data='{"text":"'+msg+'"}', verify=False, timeout=2)
    except requests.exceptions.RequestException as e:
        logging.error('Slack reachablility issue : '+ str(e))
        print('No Slacking:-->\t'+msg)
        return

def find_vaccine(query,headers):

    while True:
        try:
            with httpx.Client(http2=True, verify=False, proxies=proxies, timeout=10.0) as client:
                response = client.get(cowinURL, params=query, headers=headers)
                logging.info('Response time : ' + str(response.elapsed.total_seconds()))
                # print(response.http_version)
                #print('\x1b[1;32;40m' + ' Mission Hunt Response time : ' + str(response.elapsed.total_seconds()) + '\x1b[0m', end='\r', flush=True)
                availability = response.json()
                print(str(availability))
                time.sleep(3) #default Sleep for 10 Sec

        except requests.exceptions.RequestException as e:
            logging.error('Unable to reach Cowin Gateway ' + str(e))

            '''try:
                print('Checking availablity')
                response = requests.get(cowinURL, params=query, proxies=proxies, verify=False, headers=headers)
                logging.info('Response time : '+str(response.elapsed.total_seconds()))
                #print('\x1b[1;32;40m'+' Response time : '+str(response.elapsed.total_seconds())+'\x1b[0m', end='\r', flush=True)
                availability = json.loads(response.content)

                print(str(availability))
                for each in availability['centers']:
                    print(availability['name'])
                    print(availability['sessions']['available_capacity'])
                time.sleep(10) #default Sleep for 10 Sec

            except requests.exceptions.RequestException as e:
                logging.error('Unable to reach Cowin Gateway ' + str(e))
             if response == 200 :
                availability = response.json()
                for each in availability['centers']:
                    print(availability['name'])
                    print(availability['sessions']['available_capacity'])
            time.sleep(10) #default Sleep for 10 Sec '''


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
    #pincode = input('\nEnter Pincode: ')

    #setup parameters
    query = {'district_id': '363','date': '15-05-2021'}

    availablity=find_vaccine(query,headers)
    message_slack(availablity)

if __name__ == '__main__':
    main()