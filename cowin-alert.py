#!/usr/bin/python
# -*- coding: utf-8 -*-


import requests
import logging
import time
import httpx
from telegram.ext import Updater, CommandHandler
import re
from datetime import date

# Setting up log files
logging.basicConfig(filename='requests.log', level=logging.DEBUG,
                    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# setting up Global variables
cowinURLdist = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict'
cowinURLPin = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin'

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
today = date.today()
search_date = today.strftime("%d-%m-%Y")
# Mumbai = 995
# East Delhi = 145
# Pune = 363
#distquery = {'district_id': '363', 'date': search_date}
#pinquery = {'pincode': '110091', 'date': search_date}

'''
To send messages to telegram
you can use any other channel to send messages like Slack/whatsapp/email
just send 'msg' which stores your customized results
'''
def message_telegram(msg, chat_id):
    msg = str(msg)
    try:
        print(msg)
        #telegram_send.send(messages=[msg])
    except requests.exceptions.RequestException as e:
        logging.error('Telegram reachability issue : ' + str(e))
        print('No Telegram:-->\t' + msg)
        return

def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi! Please send command /pincode followed by your pin to get notification \n if you know your district ID send command /distid followed by three digit code ')

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help! if you know your district ID send command /distid followed by three digit code')


'''
This function will find vaccine 
'''
def find_vaccine(query, headers, cowinURL, age):
        try:
            with httpx.Client(http2=True, verify=False) as client:
                response = client.get(cowinURL, params=query, headers=headers)
                logging.info('Response time : ' + str(response.elapsed.total_seconds()))
                # print(response.http_version)
                availability = response.json()
                print('*********************************** ++++++++ ********************')
                print(type(availability))
                centers = availability['centers']
                for key in centers:
                    print('******* '+key['name']+' ********')
                    msg = 'Name: <b>' + key['name'] + '</b> Address: ' + key['address'] + ' Fees: ' + key['fee_type']
                    for capacity in key['sessions']:
                        print(str(capacity['available_capacity'])+' on date '+str(capacity['date'])+'')
                        if capacity['available_capacity'] > 0 and capacity['min_age_limit'] == age:
                            msg = msg + ' Vaccine Brand: ' + str(capacity['vaccine']) + ' For Age: ' + str(capacity['min_age_limit']) + ' Available : ' + str(capacity['available_capacity']) + ' *On Date* ' + str(capacity['date'])
                            return msg
                            logging.info(msg)
                            #message_telegram(msg)
                            #print(msg)
        except requests.exceptions.RequestException as e:
            logging.error('Unable to reach Cowin Gateway ' + str(e))
        #exit(0)

def pincode(update, context):
    pincode = update.message.text  # need to validate pincode
    pinquery = {'pincode': pincode, 'date': search_date}
    result = find_vaccine(pinquery, headers, cowinURLPin)
    update.message.reply_text(result)

def distcode(update, context):
    distcode = update.message.text  # need to validate distcode
    distquery = {'district_id': distcode, 'date': search_date}
    result = find_vaccine(distquery, headers, cowinURLdist)
    update.message.reply_text(result)

def main():
    # setup parameters
    updater = Updater('1773514624:AAHsFg3_fb2IGiwcRipeX-au6v_PS-MsUwM', use_context=True)
    dp = updater.dispatcher
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler('pincode', pincode))
    dp.add_handler(CommandHandler('distcode', distcode))
    # log all errors
    #dp.add_error_handler(error)
    updater.start_polling()
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
