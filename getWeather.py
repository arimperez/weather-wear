#!/usr/bin/python
# -*- coding: utf-8 -*-

##############################
#Written By Ari Perez
#Started: April 24, 2017
#Description: Given location program outputs temperature data
##############################

import requests
from bs4 import BeautifulSoup

found = False

real_temp = 0
feel_temp = 0
wind_value = 0

#Get User Input
state = ""
country = raw_input("Enter Country: ")
country = country.replace(" ", "-")
if country == "United-States-of-America":
    state = raw_input("Enter State: ")
    state = state.replace(" ", "-")
    country = country + "/" + state
city = raw_input("Enter City: ")
############Find code for location##############
find_location = requests.get("https://weather.codes/" + country + "/")
find_location.connection.close()
clean = BeautifulSoup(find_location.content, "html.parser")

codes = clean.find_all('dt')
names = clean.find_all('dd')
#table = table.split("<dl>")
for i in range(len(names)-1):
    names[i] = names[i].get_text()
    if (city in names[i]):
        found = True
        codes[i] = codes[i].get_text()
        break
################################################


if (found == True):
    page = requests.get("https://weather.com/en-CA/weather/today/l/"+ codes[i] +":1")

    soup = BeautifulSoup(page.content, "html.parser")

    #figure out what all this means, and what the options are
    #generalWeather = ["Partly Cloudy", "Mostly Cloudy", "Showers", "Rain", "Clear"]
    rain = ["Showers", "Rain", "Thunderstorm", "Hail", "Rain Shower", "Showers in the Vicinity"]

    try:
        wind_speed_display = soup.find_all(id = "dp0-details-wind")[0].get_text()

        wind_speed = wind_speed_display.split(" ")
        if (wind_speed[1].isdigit()):
            #Gets actual number value to determine what to wear
            wind_value = int(wind_speed[1])

        #Get data for temperature outside
        real_temp_text = soup.find_all(class_= "today_nowcard-temp")[0].get_text()

        real_temp = int(real_temp_text[0:len(real_temp_text)-1])

        #Get info like Cloudy or Scattered Showers
        looks_like = soup.find_all(class_= "today_nowcard-phrase")[0].get_text()

        #Get the temperature it feels like
        feel_temp_text = soup.find_all(class_= "deg-feels")[0].get_text()


        feel_temp = int(feel_temp_text[0:len(feel_temp_text)-1])

        #later = soup.find_all(class_ = "today-daypart-content")[0].get_text()

        #Get weather later today
        later = soup.find_all(class_ = "today-daypart-title")[0].get_text()
        later_phrase = soup.find_all(class_ = "today-daypart-wxphrase")[0].get_text()
        later_weather = soup.find_all(class_ = "today-daypart-temp")[0].get_text()
        later_temp = int(later_weather[0:len(later_weather)-1])



        #######################Display Data###########################
        print("--Weather Right Now--")
        print(names[i])
        print(looks_like)
        print("Wind: " + wind_speed_display)
        print("Temperature Outside: %d °C" % real_temp)
        print("Feels Like: %d °C" % feel_temp)

        print("\n--Weather " + later + "--")
        print(later_phrase)
        print("Temperature: %d °C" % later_temp)

        print("\nYou should Wear")

        if (feel_temp >= 30):
            print("Warning! Too Hot. Limit outside activities")
            print("T-Short and Shorts (or similar summer attire) and a hat")


        elif (feel_temp >= 16 and feel_temp < 30):
            print("T-Short and Shorts (or similar summer attire) and a hat")


        elif (feel_temp <=15 and feel_temp >12):

            print("Long pants and a tshirt (may consider sweater)")


        elif (feel_temp <= 12 and feel_temp > 7):
            print("Tshirt and Sweater, Long pants")


        elif (feel_temp <= 8 and feel_temp > 3):
            print("Long sleeved shirt, sweater/thin jacket")

        elif (feel_temp <= 3 and feel_temp > -10):
            print("A warm Jacket, a hat and gloves, long sleeved shirt, long pants")


        elif (feel_temp <= -10 and feel_temp > -25):
            print("A warm Sweather, A winter jacket, a hat, gloves and a scarf, long sleeved shirt")


        elif (feel_temp <= -25):
            print("~Warning~ Do not go outside!")
            print("A warm Sweather, A winter jacket, a hat, gloves and a scarf, long sleeved shirt")

        if (wind_value >= 25):
            print("\nHigh Wind Warning: You might consider wearing slightly warmer clothes")
        if (looks_like in rain):
            print("\nRain Warning: Consider an umbrella or rain jacket")

    except:
        print("Connection Error - Try Again Later")

else:
    print("Location Not found")
