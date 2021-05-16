# Cowin-alert For Any Location

This is custom bot script which will alert you on telegram bot if there is any vaccine slot available in provided area.
You customise it to filer as you need.

## Setting up:
### On your Phone
- Open your telegram and search for @botFather
- Type `/newbot`
- Enter name of the bot (it should end with '_bot')
- You will receive a token 

### On your machine 
- Run `sudo pip3 install httpx[http2]`
- Run `sudo pip3 install telegram-send`
- Run `telegram-send --configure`
- Enter the token received from botFather
- It will generate a token which you need to send to the newly created channel

[Refer this if you face any issue](https://medium.com/@robertbracco1/how-to-write-a-telegram-bot-to-send-messages-with-python-bcdf45d0a580)

## Running Script
Inside script 'cowin-alert.py'
- Change age on line 48 according to your age limit
- Change district ID on line 73 (by default its Pune '363'); you can get your district id from cowin website.

Be safe and get vaccinated !!

