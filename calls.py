import requests
import json 
from ip2geotools.databases.noncommercial import DbIpCity # used to get location from public ip address
import public_ip as ip # used to get public ip address

country = 'US'
appid = 'ffa78836e9836379d10c84b90c28728b'

def get_weather(city=None, state=None, country=country, appid=appid):
    # check if city/state passed
    if not city and not state:
        location = get_user_location()
        # request to get geo coords
        geo_coords = get_geo_coords(location[0], location[1])
        city_st_tuple = (location[0], location[1])
    else:
        city_st_tuple = (city, state)
        geo_coords = get_geo_coords(city, state, country)
        city_st_tuple = (city, state)

    lat, long = geo_coords[0], geo_coords[1]

    # request to get weather info
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={long}&appid={appid}&units=imperial')
    weather_info = res.json()

    return weather_info, city_st_tuple

def get_forecast(city=None, state=None, country=country, appid=appid):
    # check if city/state passed
    if not city and not state:
        location = get_user_location()
        # request to get geo coords
        geo_coords = get_geo_coords(location[0], location[1])
        city_st_tuple = (location[0], location[1])
    else:
        city_st_tuple = (city, state)
        geo_coords = get_geo_coords(city, state, country)
        city_st_tuple = (city, state)

    lat, long = geo_coords[0], geo_coords[1]
    # request to get geo coords
    res = requests.get(f'http://api.openweathermap.org/data/2.5/forecast/daily?lat={lat}&lon={long}&appid={appid}&cnt=7&units=imperial')
    forecast_info = res.json()
    return forecast_info, city_st_tuple

def get_geo_coords(city, state, country=country, appid=appid):
    # request to get geo coords
    geo_coords = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={city},{state},{country}&limit=1&appid={appid}')
    geo_coords = geo_coords.json()
    lat = geo_coords[0]['lat']
    long = geo_coords[0]['lon']

    return (lat, long)

def get_user_location():
    ip_add = ip.get() # gets public ip address
    res = DbIpCity.get(ip_add, api_key="free") # finds location based on public ip
    return (res.city, res.region)
###########test############

if __name__ == '__main__':
    print(get_forecast())