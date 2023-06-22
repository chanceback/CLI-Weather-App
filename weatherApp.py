import inquirer
from tabulate import * 
from yaspin import yaspin # loading icon/animation
from pyfiglet import Figlet
from calls import *
import time 

class WeatherApp:
    """
    Represents the app itself. Requires calls.py to make weather API calls.
    """
    def __init__(self) -> None:
        pass

    def run(self):
        """
        Prints welcoming messages and runs app.
        """
        f = Figlet(font='big')
        print(f.renderText('Weather App'))
        print("Hello! Welcome to the Weather App.")
        print("Try out the Favorites List for quick and easy access to frequented cities!")
        print("To add a favorite, just look for the 'Add Favorite' button in the city menu.")

        self.__main_menu()
    
    ########################
    # Menus
    ########################
    def __main_menu(self):

        while True:
            # Create menu and menu options
            nav1 = "Search for City"
            nav2 = "Favorites List"
            nav3 = "Exit"
            questions = [
            inquirer.List('cmd',
                            message="Select a command",
                            choices=[nav1, nav2, nav3],
                        ),
            ]

            # Run menu prompt and navigate based off user selection
            answers = inquirer.prompt(questions)
            cmd = answers['cmd']

            if cmd == nav1: self.__search_menu()
            elif cmd == nav2: self.__favorites_menu()
            else: break   
              
    def __search_menu(self):
        # Create menu and menu options
        nav1 = "Manual Search"
        nav2 = "Use Current Location"
        nav3 = "Back"
        questions = [
        inquirer.List('cmd',
                        message="Select a command",
                        choices=[nav1, nav2, nav3],
                    ),
        ]

        # Run menu prompt and navigate based off user selection
        answers = inquirer.prompt(questions)
        cmd = answers['cmd']

        if cmd == nav1:
            city_st_tuple = self.__get_city()
            weather_info, location = self.__call_api(city_st_tuple)
            self.__city_menu(weather_info, city_st_tuple)

        elif cmd == nav2: 
            weather_info, city_st_tuple = self.__call_api()
            self.__city_menu(weather_info, city_st_tuple)
        else: return

    def __city_menu(self, weather_info, city_st_tuple=None):
        self.__display_weather(weather_info, city_st_tuple)

        while True:
            # Create menu and menu options
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

            # Run menu prompt and navigate based off user selection
            answers = inquirer.prompt(questions)
            cmd = answers['cmd']

            if cmd == nav1: self.__display_weather(weather_info, city_st_tuple, detailed=True)
            elif cmd == nav2: 
                forecast_info, location = self.__call_api(city_st_tuple, forecast=True)
                self.__display_forecast(forecast_info)
            elif cmd == nav3: 
                self.__add_favorite(city_st_tuple[0], city_st_tuple[1])
            elif cmd == nav4: break
    
    def __favorites_menu(self):
        while True:
            # Create menu and menu options
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

            # Run menu prompt and navigate based off user selection
            answers = inquirer.prompt(questions)
            cmd = answers['cmd']

            if cmd == nav1: self.__display_favorites()
            elif cmd == nav2:
                self.__display_favorites()
                city = input("City: ")
                state = input("State: ")
                self.__remove_favorite(city, state)
            elif cmd == nav3:
                # Confirm users wishes to delete everything in list with prompt
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
            else: break
    
    ########################
    # Weather Commands
    ########################
    def __get_city(self):
        """
        Prompt user for city and state.
        """
        questions = [
            inquirer.Text('city', "City: "),
            inquirer.Text('state', "State: ")
        ]
        answers = inquirer.prompt(questions)
        return (answers['city'], answers['state'])
        
    @yaspin(text="Loading...", color="yellow")
    def __call_api(self, city_st_tuple=None, forecast=False):
        """
        Calls the weather API functions from calls.py. Will get weather or 
        forecast for current or given location.
        """
        # Get weather for current location
        if not city_st_tuple and not forecast: 
            city_data, location = get_weather()
        # Get weather for given location
        elif city_st_tuple and not forecast: 
            city_data, location = get_weather(city_st_tuple[0], city_st_tuple[1])
        # Get forecast for current location
        elif not city_st_tuple and forecast: 
            city_data, location = get_forecast()
        # Get forecast for given location
        elif city_st_tuple and forecast: 
            city_data, location = get_forecast(city_st_tuple[0], city_st_tuple[1])

        return city_data, location

    def __display_weather(self, weather_info, city_st_tuple, detailed=False):
        """
        Displays weather info in table format using tabulate. Set detailed to 
        true for about the city.
        """
        # Convert sunrise/sunset times to military time
        sunrise = time.ctime(weather_info['sys']['sunrise'])[11:16]
        sunset = time.ctime(weather_info['sys']['sunset'])[11:16]

        primary_info = [
            ['Temp', f"{round(weather_info['main']['temp'])} °F"],
            ['Feels Like', f"{round(weather_info['main']['feels_like'])} °F"],
            ['Conditions', f"{weather_info['weather'][0]['main']}: {weather_info['weather'][0]['description']}"],
            ['High/Low', f"{round(weather_info['main']['temp_max'])} / {round(weather_info['main']['temp_min'])} °F"]
        ]
        detailed_info = [
            ['Humidity', f"{weather_info['main']['humidity']}%"],
            ['Pressure', f"{weather_info['main']['pressure']} hPa"],
            ['Cloud Coverage', f"{weather_info['clouds']['all']}%"],
            ['Wind', f"{round(weather_info['wind']['speed'])} mph"],
            ['Visibility', f"{round(weather_info['visibility']*0.00062137)} mi"],
            ['Sunrise', sunrise],
            ['Sunset', sunset]
        ]
        header = [city_st_tuple[0], city_st_tuple[1]]

        info = primary_info + detailed_info if detailed else primary_info

        result = tabulate(info, header, tablefmt="grid")
        print(result)

    def __display_forecast(self, forecast_info):
        """
        Unpack forecast data into a user friendly table using tabulate.
        """
        forecast_table = []
        for date in forecast_info['list']:
            day = time.ctime(date['dt'])
            day = day[:10]
            forecast_table.append([day, f"{round(date['temp']['max'])} / {round(date['temp']['min'])}"])
        
        header = ['Day', 'High/Low °F']

        result = tabulate(forecast_table,header, tablefmt="grid")
        print(result)

    ########################
    # Favorite Menu Commands
    ########################
    def __add_favorite(self, city, state):
        """
        Add city to favorites list.
        """
        code = add_favorite(city, state)
        if code != 200:
            print("Something went wrong, could add city to list")
        else: print("Successfully added city to list")
        
    def __remove_favorite(self, city, state):
        """
        Remove city from favorites list.
        """
        code = remove_favorite(city, state)
        if code != 200:
            print("Something went wrong, could not remove city")
        else: print("Successfully removed city from favorites")

    def __clear_favorites(self):
        """
        Clear favorites list.
        """
        code = clear_favorites_list()
        if code != 200:
            print("Something went wrong, could not clear list")
        else: print("Successfully cleared list")

    def __display_favorites(self):
        """
        Display favorites list in table using tabulate.
        """
        favs = get_favorites_list()
        
        # return if list is empty.
        if not favs:
            print('List is empty!')
            return
        
        places_table = []
        for place in favs:
            places_table.append([place['city'], place['state']])
        header = ['City', 'State']
        result = tabulate(places_table, header, tablefmt='grid')
        print(result)


def main():
    app = WeatherApp()
    app.run()

if __name__ == "__main__":
    main()
    