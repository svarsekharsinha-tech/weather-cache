import urllib.request,urllib.parse,urllib.error
import json
import time
import sqlite3

conn=sqlite3.connect('weather.db')
cur=conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS weather (city TEXT PRIMARY KEY, temperature REAL, humidity INTEGER, description TEXT);')
f=open('cities.txt')
count=0
weather_codes = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    51: "Light drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    80: "Slight rain showers",
    95: "Thunderstorm",
}
for line in f:
    city=line.rstrip()
    cur.execute('SELECT * FROM weather WHERE city=?',(city,))
    row=cur.fetchone()
    if not city:
        continue
    if row is not None:
        continue
    else:
        serviceurl='https://geocoding-api.open-meteo.com/v1/search?'
        url=serviceurl+urllib.parse.urlencode({'name':city,'count':1})
        try:
            info=urllib.request.urlopen(url).read().decode()
            data=json.loads(info)
        except Exception as e:
            print("Error retrieving data for", city, ":", e)
            continue
        if 'results' not in data or len(data['results'])==0:
            print("No results found for", city)
            continue
        serviceurl2='https://api.open-meteo.com/v1/forecast?'
        url2=serviceurl2+urllib.parse.urlencode({'latitude':data['results'][0]['latitude'],'longitude':data['results'][0]['longitude'],'current':'temperature_2m,relative_humidity_2m,weather_code'})
        try:
            info2=urllib.request.urlopen(url2).read().decode()
            data2=json.loads(info2)
        except Exception as e:
            print("Error retrieving weather data for", city, ":", e)
            continue
        if 'current' not in data2:
            print("No current weather data available for", city)
            continue
        temperature=data2['current']['temperature_2m']
        humidity=data2['current']['relative_humidity_2m']
        weather_code=data2['current']['weather_code']
        description=weather_codes.get(weather_code, "Unknown")
        cur.execute('INSERT INTO weather (city, temperature, humidity, description) VALUES(?,?,?,?)',(city,temperature,humidity,description))
        conn.commit()
        count+=1
    if count%10==0:
        print("Pausing for a bit...")
        time.sleep(5)
f.close()
conn.close()
