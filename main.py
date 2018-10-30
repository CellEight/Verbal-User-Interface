#!/usr/bin/env python3
import speech_recognition as sr
import pyaudio, wave, os, sys
import time as t
import csv
from urllib.request import urlopen
import re
import urllib.error
import requests
import json
import pyowm

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

def speak(text):
    os.system("pico2wave " + " --wave=buffer.wav \""+text+"\" ")
    playSound("buffer.wav")

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

def respond(data):
    data = data.lower()

    if "how are you" in data:
        speak("I am fine")
    elif "what is your name" in data:
        speak("My name is winter mute")
    elif "what colour is the sky above the port" in data:
        speak("The sky above the port is the color of television, tuned to a dead channel")
    elif "what time is it" in data:
        speak(t.ctime())
    elif "where is" in data:
        data = data.split(" ")
        data = data[2:]
        location = ""
        for word in data:
            location = location + word + "+"
        speak("Hold on, I will show you where " + location.replace("+", " ") + " is.")
        os.system("firefox https://www.google.nl/maps/place/" + location + "/&amp;")
    elif "google" in data:
        data = data.split(" ")
        search = ""
        print(data)
        for word in data[1:]:
            search = search + word + "+"
        search = search[:len(search)-1]
        speak("Searching for "+search.replace("+", " "))
        os.system("firefox https://www.google.co.uk/search?q="+search)
    elif "what is the weather" in data:
        loc = getLocation()
        weather = getWeather(loc)
        speak("The Temprature in "+str(loc[2])+", "+str(loc[3])+"is" +str(wea.get_temperature(unit='celsius')['temp'])+ " degrees celsius And the Outlook is "+ wea.get_detailed_status())
    else:
        data = data.translate(str.maketrans({"-":  r"\-","]":  r"\]","\\": r"\\","^":  r"\^","$":  r"\$","*":  r"\*",".":  r"\."}))
        data = data.split(" ")
        query = "https://api.wolframalpha.com/v1/spoken?i="
        for word in data:
            query = query + word + "+"
        query = query[:len(query)-1]
        query = query + "&appid=PH6A46-W3YT2RUAX8"
        print(query)
        #query = "http://olyblog.net/robots.txt"
        response = " Not known"
        try:
            response = urlopen(query).read()
        except urllib.error.URLError as e:
            print(e.reason)
        except urllib.error.HTTPError as e:
            print(e.code + ": " + e.read())

        response = str(response)[1:].strip('\'').lower()
        if "the answer is " in response:
            response = response[14:]
        response = re.sub('\\\\x[A-Za-z0-9_.][A-Za-z0-9_.]',' ',response)
        response = re.sub('\((.*?)\)', '', response)
        response = re.sub('\s{2,}', ' ', response)
        response = re.sub('^"', ' ', response)
        response = re.sub('"$', ' ', response)
        print(response)
        speak(response)

def main():
    r = sr.Recognizer()

    #with sr.AudioFile(WAVE_OUTPUT_FILENAME) as source:
    #        audioData = r.record(source)


    while True:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            audioData = r.listen(source)
            print("Got audio, now to Recognize...")
            try:
                text = r.recognize_google(audioData)
                respond(text)
            except sr.UnknownValueError:
                print("Undecipherable")
            except sr.RequestError as e:
                print("Error: {0}".format(e))

if __name__ == '__main__':
    main()
