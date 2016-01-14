#!/usr/bin/python
import time
import datetime
import requests
from lxml import html
import win32api
import re




# Change these values to your desired cricket page.
# Currently set to cricket.yahoo.com
BASE_URL = "https://cricket.yahoo.com/"
SLEEP_INTERVAL = 30 #seconds
XPATH_SELECTORS = ['//*[@id="lms-top-left-markup"]/text()']
#ITEMS is a list of lists, storing ASINs and their lowest prices recorded
ITEMS = [['cricket-live-score-australia-vs-india_191950',0]] #Entry Price


def alert_win32(score,wickets,id):
    win32api.MessageBox(0,"Alert {1} wicket(s) has fallen!! Current Score {0}".format(score,wickets),'Match {}'.format(id),0x00001000)
    
while True:
    #item[0] is the number of wickets
	for index, item in enumerate(ITEMS):
		r = requests.get(BASE_URL + item[0])
		tree = html.fromstring(r.text)
		#print("Retreiving current score for match '{}'".format(item[0]))
                for XPATH_SELECTOR in XPATH_SELECTORS:
                    try:
                            #We have to strip the dollar sign off of the number to cast it to a float
                            #price = float(tree.xpath(XPATH_SELECTOR)[2]/text[1:])
                            score = tree.xpath(XPATH_SELECTOR)[0].strip().replace(',','')
                            wickets= int(re.split('\/',score)[1])
                            print("[{}]: Score {}".format(datetime.datetime.now(),score))
                    except IndexError:
                            #print("Didn't find the 'score' element, trying again")
                            continue
                    if  wickets > item[1]: #If wicket has fallen
                            newwickets=wickets-ITEMS[index][1]
                            print(" '{0}' new Wicket(s) have fallen from  '{1}'!! Current Score '{2}'.".format(newwickets,item[1],score))
                            ITEMS[index][1]= wickets
                            alert_win32(score,newwickets,item[0])
                            break
                    elif wickets < item[1]: # Innings change
                            ITEMS[index][1]= wickets
                            alert_win32("Innings Changed",score)
                            print("Innings Changed ..resetting wickets fallen to '{0}' CurrentScore '{1}'".format(wickets,score) )
                            break
                    else :
                            #print("No new wicket(s) have fallen.. Current Score '{}'. Ignoring...".format(score))
                            break; #No Need to parse using another XPATH

	#print "Sleeping for {} seconds".format(SLEEP_INTERVAL)
	time.sleep(SLEEP_INTERVAL)
