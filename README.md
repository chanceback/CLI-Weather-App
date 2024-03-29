# CLI-Weather-App
## About
A weather app that operates entirely within the terminal. 

Can be used for getting current weather information as well as forecast data.

Requires a [OpenWeather API Key](https://openweathermap.org/api) to function properly.

## Screenshots

Home Menu:
![Home Menu](https://drive.google.com/uc?export=view&id=1XYjXW7V8zdZVux98Ws00nMp4ygHFJ4P5)

Search Menu - performing a search using current location:
![search menu](https://drive.google.com/uc?export=view&id=1IERC-UGurO_bsyxnoX0LujDuEbuptrgc)

Results of a location search:
![search results](https://drive.google.com/uc?export=view&id=1HvIL11RWH8dgVn9fq289sOg9iL1K_rLT)

Detailed View available for the user:
![Detailed View](https://drive.google.com/uc?export=view&id=1kNOTsAEpypSczyp_xEtoU0hXElYcUYMR)

Weekly Forecast view:
![Weekly Forecast](https://drive.google.com/uc?export=view&id=1XHZ0TJK-OBmz9CWfb0TW9uv2uVndjihc)

Favorites List Menu (Microservice implemented by partner):
![Favorites List](https://drive.google.com/uc?export=view&id=1Zqx7nQFZmXugjXRh5CaXOphTBSWNXd6h)


## Usage Setup
To run locally, first download and unzip the file. 

From there, start up the Favorites List microservice in the background or a separate terminal by calling `python3 fav_ms.py`.

It should run on localhost:5000.

Next, start up the weather app by running `python3 weatherApp.py`. 

The home menue should appear, and you are free to look up the desired wewather information!
