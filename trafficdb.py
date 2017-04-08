import sqlite3
import sys
import datetime
import simplejson, urllib
import time

#insert google apikey here - requires registering with google to use
apikey = ''
sql = sqlite3.connect('traffic.db')
cur = sql.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS tabley(year TEXT, month TEXT, day TEXT, hour TEXT, minutes TEXT, dayofweek TEXT, driving_time_minutes TEXT)')

while(1):
    year = time.strftime("%Y")
    month = time.strftime("%m")
    day = time.strftime("%d")
    hour = time.strftime("%H")
    minu = time.strftime("%M")
    dayofweek = time.strftime("%A")
    curtime = time.strftime("%Y %m %d %H:%M:%S %A")
    #only run from 5am to 8pm
    if hour >= 5 or hour <= 20:
        daycheck = time.strftime("%p")
        if daycheck == "AM":
            #random addresses used
            url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=45.636841,-122.582197&destinations=45.486553,-122.800332&mode=driving&language=en-EN&sensor=false&departure_time=now&traffic_model=best_guess&units=imperial&key=" + apikey
        elif daycheck == "PM":
            url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=45.486553,-122.800332&destinations=45.636841,-122.582197&mode=driving&language=en-EN&sensor=false&departure_time=now&traffic_model=best_guess&units=imperial&key=" + apikey

        result= simplejson.load(urllib.urlopen(url))
        driving_time_in_mins = result['rows'][0]['elements'][0]['duration_in_traffic']['text']
        driving_time = int(filter(str.isdigit, driving_time_in_mins))
        #log to database

        cur.execute('SELECT * FROM tabley')
        cur.execute('INSERT INTO tabley VALUES(?, ?, ?, ?, ?, ?, ?)', [year, month, day, hour, minu, dayofweek, driving_time])
        sql.commit()
        print curtime, driving_time_in_mins, daycheck 
        time.sleep(60)

        #option to turn off logging if traffic is minimal
        '''if driving_time == "31 mins" or driving_time == "32 mins" or driving_time == "33 mins" or driving_time == "34 mins" or driving_time == "35 mins" or driving_time == "36 mins" or driving_time == "29 mins":
            print ('no traffic, waiting 10 minutes')
            time.sleep(600)        
        else:
            time.sleep(60)'''
    else:
        #check again in 15 if time isn't between 5am-8pm
        time.sleep(900)
