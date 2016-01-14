#!/usr/bin/python
import time
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from lxml import html
import ConfigParser
import win32api

# Create a creds file with user and password information
config = ConfigParser.RawConfigParser()
config.read("creds")
email_user = config.get('email','user')
email_pass = config.get('email','pass')
#BASE_URL = config.get('url')



# Change these values to your desired sale page (the selector and price check were tested on Amazon).
BASE_URL = "http://www.amazon.in/exec/obidos/ASIN/"
SMTP_URL = "smtp.gmail.com:587"
SLEEP_INTERVAL = 60*10 #seconds
XPATH_SELECTORS = ['//*[@id="priceblock_ourprice"]/text()','//*[@id="priceblock_saleprice"]/text()']
#ITEMS is a list of lists, storing ASINs and their lowest prices recorded
ITEMS = [['B00VBGWUKU',75150]] #Entry Price

def send_email(price,drop,id):
    global BASE_URL

    try:
        s = smtplib.SMTP(SMTP_URL)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(email_user, email_pass)
    except smtplib.SMTPAuthenticationError,e:
        #print("Failed to login : {}").format(str(e))
        print("Failed to login")
    else:
        print("Logged in! Composing message..")
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Price Alert - {}".format(price)
        msg["From"] = email_user
        msg["To"] = email_user
        text = "The price is currently {0} !! A drop of price {1}!! URL to salepage: {2}".format(price,drop, BASE_URL+id)
        part = MIMEText(text, "plain")
        msg.attach(part)
        s.sendmail(email_user, "abhinav56321@gmail.com", msg.as_string())
        print("Message has been sent.")

def alert_win32(price,drop,id):
    win32api.MessageBox(0,"Alert Drop in Price!!: {1} Current Price {0}".format(price,drop),'Amazon ASIN{}'.format(id),0x00001000)
    
while True:
    #item[0] is the item's ASIN while item[1] is that item's minimum price
	for index, item in enumerate(ITEMS):
		r = requests.get(BASE_URL + item[0])
		tree = html.fromstring(r.text)
		print("Retreiving price for ProductId '{}'".format(item[0]))
                for XPATH_SELECTOR in XPATH_SELECTORS:
                    try:
                            #We have to strip the dollar sign off of the number to cast it to a float
                            #price = float(tree.xpath(XPATH_SELECTOR)[2]/text[1:])
                            price = float(tree.xpath(XPATH_SELECTOR)[0].strip().replace(',',''))
                    except IndexError:
                            print("Didn't find the 'price' element, trying again")
                            continue
                    if price < item[1]: #If price drops then send mail
                            print("Price is '{0}'for productId ''{1}!! Trying to send email.".format(price,item[0]))
                            drop=ITEMS[index][1]-price
                            ITEMS[index][1]= price
                            send_email(price,drop,item[0])
                            #alert_win32(price,drop,item[0])
                            break
                    else:
                            print("Price is '{}'  >= '{}'. Ignoring...".format(price,item[1]))
                            break; #No Need to parse using another XPATH

	print "Sleeping for {} seconds".format(SLEEP_INTERVAL)
	time.sleep(SLEEP_INTERVAL)
