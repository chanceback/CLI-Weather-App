import requests
import json 
from ip2geotools.databases.noncommercial import DbIpCity # used to get location from public ip address
import public_ip as ip # used to get public ip address

country = 'US'
appid = '5c473fac0bf570ae74bd2aff29b8a8ed'

def get_weather_name(city, state, country=country, appid=appid):
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city},{state},{country}&appid={appid}&units=imperial')
    weather_info = res.json()
    return weather_info

def get_weather_location():
    ip_add = ip.get() # gets public ip address
    res = DbIpCity.get(ip_add, api_key="free") # finds location based on public ip
    weather_info = get_weather_name(res.city, res.region, res.country) # gets weather info from current location
    return weather_info

def get_weather_forecast(city, state, country=country, appid=appid):
    res = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?q={city},{state},{country}&appid={appid}&units=imperial')
    weather_info = res.json()
    return weather_info

###########test############

if __name__ == '__main__':
    print(get_weather_forecast('Denver', 'CO'))