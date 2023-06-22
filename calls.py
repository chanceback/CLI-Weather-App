import requests
import public_ip as ip
from ip2geotools.databases.noncommercial import DbIpCity
from api_key import *

country = 'US'
appid = get_key() # Open Weather API key
FAVORITES_PORT = 5000 # PORT of Microservice

########################
# Weather Calls
########################
def get_weather(city=None, state=None, country=country, appid=appid):
    """
    Calls weather API for a city and returns weather data in JSON format.
    """
    # Check if city/state received else use current location
    if not city and not state:
        location = get_user_location()
        geo_coords = get_geo_coords(location[0], location[1])
        city_st_tuple = (location[0], location[1])
    else:
        geo_coords = get_geo_coords(city, state, country)
        city_st_tuple = (city, state)

    lat, long = geo_coords[0], geo_coords[1]

    # Request weather info from Open Weather API
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={long}&appid={appid}&units=imperial')
    weather_info = res.json()

    return weather_info, city_st_tuple

def get_forecast(city=None, state=None, country=country, appid=appid):
    """
    Calls weather API for a city and returns forecast data in JSON format.
    """
    # Check if city/state received else use current location
    if not city and not state:
        location = get_user_location()
        geo_coords = get_geo_coords(location[0], location[1])
        city_st_tuple = (location[0], location[1])
    else:
        city_st_tuple = (city, state)
        geo_coords = get_geo_coords(city, state, country)
        city_st_tuple = (city, state)

    lat, long = geo_coords[0], geo_coords[1]

    # Request forecast info from Open Weather API
    res = requests.get(f'http://api.openweathermap.org/data/2.5/forecast/daily?lat={lat}&lon={long}&appid={appid}&cnt=7&units=imperial')
    forecast_info = res.json()

    return forecast_info, city_st_tuple

def get_geo_coords(city, state, country=country, appid=appid):
    """
    Calls weather API for a city and returns geo coordinates of the location.
    """
    # request to get geo coords
    geo_coords = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={city},{state},{country}&limit=1&appid={appid}')
    geo_coords = geo_coords.json()
    lat = geo_coords[0]['lat']
    long = geo_coords[0]['lon']

    return (lat, long)

def get_user_location():
    """
    Gets user location using public IP address
    """
    ip_add = ip.get()
    res = DbIpCity.get(ip_add, api_key="free")

    return (res.city, res.region)

########################
# Favorite Menu Calls
########################
def get_favorites_list():
    """
    Requests favorite list from partner's microservice.
    """
    res = requests.get(f'http://localhost:{FAVORITES_PORT}/get_locations')
    favs = res.json()['locations']

    return favs

def clear_favorites_list():
    """
    Requests to clear favorites list from partner's microservice.
    """
    res = requests.delete(f'http://localhost:{FAVORITES_PORT}/clear_data')
    return res.status_code

def add_favorite(city, state):
    """
    Requests to add new city to favorites list from partner's microservice.
    """
    data = {
            'city': city,
            'state': state
            }
    res = requests.post(f'http://localhost:{FAVORITES_PORT}/add_location', json=data)
    return res.status_code

def remove_favorite(city, state):
    """
    Requests to remove city in favorites list from partner's microservice.
    """
    data = {
            'city': city,
            'state': state
            }
    res = requests.delete(f'http://localhost:{FAVORITES_PORT}/delete_location', json=data)
    return res.status_code


if __name__ == '__main__':
    print(get_weather())
    