
import requests
import json
from pprint import pprint


key = "e35e9e9cf136ac8f16d02c1247ba7933"

city_name = input("Enter City Name: ")

url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={key}&units=metric"

response = requests.get(url)

data = response.json()

city = data['name']
temp = data['main']['temp']
humidity = data['main']['humidity']
pressure = data['main']['pressure']
description = data['weather'][0]['description']


print("\nWEATHER DATA".center(30, "*"))

print(f"\n City Name                : {city}")
print(f"\n Temprature               : {temp}°C")
print(f"\n Humidity                 : {humidity}%")
print(f"\n Pressure                 : {pressure} hPa")
print(f"\n Weather                  : {description}")
