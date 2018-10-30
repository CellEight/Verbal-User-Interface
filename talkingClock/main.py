#!/usr/bin/env python3
import speech_recognition as sr
import pyaudio, wave, os, sys
import time as t
import requests
import json
import pyowm
import feedparser
from oauth2client import client
from googleapiclient import sample_tools

p = pyaudio.PyAudio()

def playSound(filename):
    wf = wave.open(filename)
    chunk = 1024
    stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate = wf.getframerate(),
                    output = True)
    data = wf.readframes(chunk)
    while data:
        stream.write(data)
        data = wf.readframes(chunk)
    print('Done')
    return

def speak(text):
    os.system("pico2wave --wave=buffer.wav \""+text+"\" ")
    playSound("buffer.wav")

def playAlarm():
    #Show dialouge box and play alarm sound until users confirms message
    #Say morning message
    time = t.strftime("%I:%M %p")
    date = t.strftime("%A %d %B %Y")
    loc = getLocation()
    wea = getWeather(loc)
    morning ="Good Morning Lewis. It is "+time+" on "+date+". "+"The Temprature in "+str(loc[2])+", "+str(loc[3])+"is" +str(wea.get_temperature(unit='celsius')['temp'])+ " degrees celsius And the Outlook is "+ wea.get_detailed_status()+". "
    """schedule = getSchedule()
    morning += "Your schedule is as follows. "
    for item in schedule:
        morning += item[0]+ " " + item[1] + " in " + item[3] +". "
    #[{Time}, {event}, {location}]"""
    headlines = getHeadlines()
    morning += "Here are the Headlines from your newsfeed. "
    for headline in headlines:
        morning += headline['title'] + ", " + headline['summary'] + " "
    speak(morning)
    return
"""
def getSchedule():
    #Returns a list of 3-tuples for each item on google cal for the day
     service, flags = sample_tools.init(
        argv, 'calendar', 'v3', __doc__, __file__,
        scope='https://www.googleapis.com/auth/calendar.readonly')
    try:
        page_token = None
        while True:
            calendar_list = service.calendarList().list(
                pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                print(calendar_list_entry['summary'])
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break
    except client.AccessTokenRefreshError:
        print('The credentials have been revoked or expired, please re-run'              'the application to re-authorize.')
    return
"""
def getHeadlines():
    #Returns a list of headline strings taken either from Ft.com or a RSS feed
    feed = feedparser.parse('http://www.wsj.com/xml/rss/3_7085.xml')
    return feed['items']

def getCurrentTime():
    rawTime = t.localtime()
    return (str(rawTime[0])+"-"+str(rawTime[1])+"-"+str(rawTime[2]),rawTime[6],(rawTime[3],rawTime[4]))

def getLocation():
    """Uses IP address to determine location and returns a 5-tuple ({latitude},{longitude},{city},{country},{country-code})"""
    send_url = 'http://freegeoip.net/json'
    r = requests.get(send_url)
    j = json.loads(r.text)
    return (j['latitude'],j['longitude'],j['city'],j['country_name'],j['country_code'])

def getWeather(loc):
    owm = pyowm.OWM('532afff446ea564793b7b3bcba239589')
    obs = owm.weather_at_coords(loc[0],loc[1])
    w = obs.get_weather()
    return w

# Main loop(Should wrap in function)
def main():
    alarms = [('',2,(10,41),'')] # To be a list of 3-tuples ({Date},{Day of the week}, {Time}, {Last Played})
    run = True
    while run:
        i = 0
        while i < len(alarms):
        #for alarm in alrams:
            now = getCurrentTime()
            if alarms[i][0] == '':
                if alarms[i][1] == now[1] and alarms[i][2][0] <= now[2][0] and alarms[i][2][1] <= now[2][1] and alarms[i][3] != now[0]:
                    print(alarms[i],now)
                    playAlarm()
                    alarms[i][3] = now[0]
            elif alarms[i][0] == now[0] and alarms[i][1] == now[1] and alarms[i][2][0] <= now[2][0] and alarms[i][2][1] <= now[2][1] and alarms[i][3] != now[0]:
                playAlarm()
                alarms[i][3] = now[0]
            i += 1
        #Listen for Verbal instruction from user

if __name__ == '__main__':
    main()
