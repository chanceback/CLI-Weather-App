import typer # to get city/state accurately... not sure how much my app needs typer atm
import inquirer # to provide limited choices (buttons)
import pyfiglet # ascii art used to create big letters
import tabulate # for tables
import yaspin # loading icon/animation

from calls import *

import time # for time conversions

class WeatherApp:
    """
    Represents the app itself.
    """
    def __init__(self) -> None:
        self._favorite_list = []

    def run(self):
        print("Greeting")
        self.__main_menu()
    
    def __main_menu(self):
        # List options:
        # Search for City
        # Favorite List
        # QUIT Exit Program
        while True:
            nav1 = "Search for City"
            nav2 = "Favorites List"
            nav3 = "Exit"
            
            questions = [
            inquirer.List('cmd',
                            message="Select a command",
                            choices=[nav1, nav2, nav3],
                        ),
            ]
            answers = inquirer.prompt(questions)
            cmd = answers['cmd']

            if cmd == nav1: self.__search_menu()
            elif cmd == nav2: self.__favorites_menu()
            else: break   
              
    def __search_menu(self):
        # List options:
        # Manual Search
        # Use current location
        # Back to Main Menu - Exit -- OR just don't include this...
        nav1 = "Manual Search"
        nav2 = "Use Current Location"
        nav3 = "Back"
        
        questions = [
        inquirer.List('cmd',
                        message="Select a command",
                        choices=[nav1, nav2, nav3],
                    ),
        ]
        answers = inquirer.prompt(questions)
        cmd = answers['cmd']

        if cmd == nav1:
            # Get user input for city
            # Get city data via API
            # Navigate to city menu
            city_st_tuple = self.__get_city()
            weather_info, location = self.__call_api(city_st_tuple)
            self.__city_menu(weather_info, city_st_tuple)

        elif cmd == nav2: 
            weather_info, city_st_tuple = self.__call_api()
            self.__city_menu(weather_info, city_st_tuple)
        else: return

    def __city_menu(self, weather_info, city_st_tuple=None):
        #List options:
        # Detailed View
        # Weekly Forecast
        # Add to Favorites
        # Back to Main Menu
        self.__display_weather(weather_info, city_st_tuple)

        while True:
            nav1 = "Detailed View"
            nav2 = "Weekly Forecast"
            nav3 = "Add to Favorites"
            nav4 = "Back"
            
            questions = [
            inquirer.List('cmd',
                            message="Select a command",
                            choices=[nav1, nav2, nav3, nav4],
                        ),
            ]
            answers = inquirer.prompt(questions)
            cmd = answers['cmd']

            if cmd == nav1: self.__display_weather(weather_info, city_st_tuple, detailed=True)
            elif cmd == nav2: 
                #print('Sorry this feature is currently unavailable through the free subscription of the weather API I\'m using.')
                forecast_info, location = self.__call_api(city_st_tuple, forecast=True)
                self.__display_forecast(forecast_info) # or maybe just pass it the city/state
            elif cmd == nav3: 
                self.__add_favorite(city_st_tuple) # or just pass city/state as well..
                print(f"Successfully added {city_st_tuple} to Favorites List!")
            elif cmd == nav4: break
    
    def __favorites_menu(self):
        # List options:
        # View List
        # Remove Favorite   ## somehow need UNDO button
        # Clear List        ## somehow incorporate UNDO button
        # Back to Main Menu
        # favorite list will not be a call to a database. The api will simply store favorites, and when one needs
        # to be added or removed I will just add/remove it from the api. Easy.
        while True:
            nav1 = "View List"
            nav2 = "Remove a City from Favorite List"
            nav3 = "Clear List"
            nav4 = "Back"
            
            questions = [
            inquirer.List('cmd',
                            message="Select a command",
                            choices=[nav1, nav2, nav3, nav4],
                        ),
            ]
            answers = inquirer.prompt(questions)
            cmd = answers['cmd']

            if cmd == nav1: self.__display_favorites()
            elif cmd == nav2:
                self.__display_favorites()
                index = input("What is the number associated with the city you would like removed? ")
                index = int(index) - 1
                self.__remove_favorite(index)
                print(f"Successfully removed city from Favorites List!")
            elif cmd == nav3:
                questions = [
                inquirer.List('cmd',
                                message="Are you sure? This action will permanently delete all cities in Favorites?",
                                choices=['Yes', 'No'],
                            ),
                ]
                answers = inquirer.prompt(questions)
                cmd = answers['cmd']
                if cmd == 'Yes':
                    self.__clear_favorites()
                print("Successfully Cleared Favorites List!")
            else: break

    def __get_city(self):
        questions = [
            inquirer.Text('city', "City: "),
            inquirer.Text('state', "State: ")
        ]
        answers = inquirer.prompt(questions)
        return (answers['city'], answers['state'])
        
    def __call_api(self, city_st_tuple=None, forecast=False):
        if not city_st_tuple and not forecast: city_data, location = get_weather()
        elif city_st_tuple and not forecast: city_data, location = get_weather(city_st_tuple[0], city_st_tuple[1])
        elif not city_st_tuple and forecast: city_data, location = get_forecast()
        elif city_st_tuple and forecast: city_data, location = get_forecast(city_st_tuple[0], city_st_tuple[1])
        return city_data, location

    def __display_weather(self, weather_info, city_st_tuple, detailed=False):
        print(city_st_tuple)
        print(f"Temp: {weather_info['main']['temp']}")
        print(f"Feels Like: {weather_info['main']['feels_like']}")
        print(f"{weather_info['weather'][0]['main']}: {weather_info['weather'][0]['description']}")

        if detailed:
            print("More details here")

    def __display_forecast(self, forecast_info):
        for date in forecast_info['list']:
            day = time.ctime(date['dt'])
            day = day[:10]
            print(f"{day}:      {date['temp']['max']}  {date['temp']['min']}")

    def __add_favorite(self, city_st_tuple):
        if len(self._favorite_list) < 10:
            self._favorite_list.append(city_st_tuple)
        else: print("Sorry Favorites List is currently full")

    def __remove_favorite(self, index):
        city = self._favorite_list[index]
        self._favorite_list.remove(city)

    def __clear_favorites(self):
        self._favorite_list.clear()

    def __display_favorites(self):
        for count, city in enumerate(self._favorite_list, 1):
            print(f'{count}: {city[0]}, {city[1]}')



def main():
    app = WeatherApp()
    app.run()

if __name__ == "__main__":
    main()