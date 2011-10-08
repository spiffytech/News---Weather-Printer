import urllib, re
from xml.dom import minidom

def getWeather(place):
    if(re.match("[a-zA-Z]+,* [a-zA-Z]{2}", place)) != None:
        city = re.search("[a-zA-Z]+ ", place).string.strip()  # Doesn't actually seperate city/state. Needs to!
        state = re.search(" [a-zA-Z]{2}", place).string.strip()
    
        print "city, state = " + city + ", " + state
    elif re.match("\d{5}", place) != None:
        zip = place
        print "zip code = ", zip
    else:
        return "Please enter a real location"


    if "city" in locals() and "state" in locals():
        content = urllib.urlopen("http://www.rssweather.com/wx/us/" + state + "/" + city + "/rss.php")
    else:
        content = urllib.urlopen("http://www.rssweather.com/zipcode/" + zip + "/wx.php")
        
    xmldoc = minidom.parse(content)
    
    try:
        pubDate = xmldoc.getElementsByTagName("pubDate")[0].firstChild.data
    except: 
        return "I can't find the weather for that city."
    pubDate = pubDate.split(" ")[4] + " GMT " + pubDate.split(" ")[5]
    summary = xmldoc.getElementsByTagName("description")[1].firstChild.data
    reply = summary + " (" + pubDate + ")"

    return reply
