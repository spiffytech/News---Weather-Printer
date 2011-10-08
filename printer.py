#!/usr/bin/env python

# Brian Cottingham
# spiffytech@gmail.com
# Spring 2009 
# Retrieves various information and sends it to a printer

import csv
import stocks
from time import strftime
import tiny
import urllib
import xml.etree.cElementTree as ET
from yweather import weather_for_zip as weather


def main():

    # Get today's weather
    zipcodes = importZips()  # For city/state lookup
    weather = getWeather(27607, zipcodes)
    print weather

    #  Get headlines
    headlines = getHeadlines()
    for headline in headlines:
        print headline + "\n"

    # Get a few stock quotes:
    for symbol in ("GOOG", "MSFT", "AAPL", "RHT"):
        print "{0}: {1}".format(symbol, stocks.get_quote(symbol))



def importZips():
    '''Imports zip codes from a file and pairs records their corresponding City, State'''
    zipcodes = {}
    reader = csv.reader(open('zipcodes.csv'), delimiter=',', quotechar='"')

    for row in reader:
        if row != []:
            zipcodes[row[0]] = row[1] + ", " + row[2]

    return zipcodes



def getWeather(zip, zipcodes):
    '''Retrieves the current weather from Yahoo Weather'''
    zip = str(zip)
    yweather = weather(zip)
    now = strftime("%I:%M %p")
    forecast = "Today's weather for {0}: {1}.\nCurrent temperature (at {2}): {3}\nToday's high: {4}\n".format(zipcodes[zip], yweather["current_condition"], now, yweather["current_temp"], yweather["forecasts"][0]["high"])


    # Define filenames for weather image
    images = {"sunny": "sunny.txt",
            "Mostly Cloudy": "partly.txt",
            "Partly Cloudy": "mostly.txt",
            "Cloudy": "cloudy.txt",
            "Fair": "sunny.txt",}

    # Get weather image
    image = ""
    try: 
        imgFile = file("images/" + images[yweather["current_condition"]])
    except: 
        imgFile = file("images/fail.txt")
    for line in imgFile.readlines():
        image += line

    return image + "\n" + forecast



def getHeadlines():
    '''Gets headlines from The Technician (technicianonline.com)'''
#    url = "http://www.technicianonline.com/se/1.312893-1.312893"
    url = "http://feeds.arstechnica.com/arstechnica/news?format=xml"
    rss = ET.parse(urllib.urlopen(url)).getroot()
    articles = rss.findall("channel/item")[:3]

    headlines = []
    for i in xrange(0, 3):
        headlines.append("{0}:\n\t{1}... \n\t{2}".format(articles[i].find("title").text, articles[i].find("description").text, tiny.tiny_url(articles[i].find("link").text)[7:]))

    return headlines



def fContents(filename):
    s = ""
    f = file(filename)
    for line in f:
        s += line

    return s


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "Exiting..."
