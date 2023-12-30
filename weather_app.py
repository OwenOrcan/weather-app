import ttkbootstrap as ttk
from PIL import Image, ImageTk
import tkinter as tk
import requests
from tkinter import messagebox

"""
kelvin_to_celsius_fahrenheit function
This function takes in one argument:
    - kelvin (int) : Temperature in Kelvin
The function performs conversions from Kelvin to both Celsius and Fahrenheit scales.
Returns:
    - celsius (float) : Temperature converted to Celsius.
    - fahrenheit (float) : Temperature converted to Fahrenheit.
Returns a tuple (celsius, fahrenheit)
"""


def kelvin_to_celsius_fahrenheit(kelvin: int):
    # Convert temperature from Kelvin to Celsius and Fahrenheit
    celsius = kelvin - 273.15
    fahrenheit = celsius * (9 / 5) + 32
    return celsius, fahrenheit


"""
get_weather_data

This function queries weather data for a given city from the OpenWeatherMap API. It parses the response and returns a
tuple with a set of weather information.

Parameters: city (str): The name of the city for which the weather data is to be retrieved. The format should be such
that it can be directly inserted into the API query.

Returns: Tuple: A tuple containing the city name, a description string of the weather, the temperature in Fahrenheit,
and the temperature in Celsius. The latter two are formatted as strings with the temperature degree and the
respective scale as value, i.e., "<value>C" or "<value>F". The weather_description is capitalized.

"""


# This function creates and sends a GET request to the OpenWeatherMap API, retrieves weather data for the provided
# city in JSON format. It extracts the weather description, the city name, and the temperature in Kelvin from the
# JSON response. The temperature in Kelvin is then converted to Celsius and Fahrenheit using the
# `kelvin_to_celsius_fahrenheit` function (Defined above). Lastly, the function returns a tuple with the city name,
# description of the weather, temperature in Fahrenheit and temperature in Celsius.
def get_weather_data(city):
    # API request to OpenWeatherMap to get weather data
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},us&APPID=07b914069d0550579f1980d1c73d8d92"
    response = requests.get(url).json()

    # Extract relevant information from the API response
    weather_description = response["weather"][0]["description"]
    city_name = response["name"]
    kelvin_temperature = response["main"]["temp"]
    celsius, fahrenheit = kelvin_to_celsius_fahrenheit(kelvin_temperature)
    celsius = f"{celsius:.0f}C"
    fahrenheit = f"{fahrenheit:.0f}F"
    weather_description = weather_description.title()
    return city_name, weather_description, fahrenheit, celsius


# WeatherApp Class
"""
Main class of the Weather Application GUI in Python.

This class is responsible for the creation, management, and functions of the GUI of the python weather application.
It uses the tkinter and ttkbootstrap libraries for the visualization of the app and to take user inputs.
It also uses the Pillow library for handling images in the application.

This class follows the principles of object-oriented programming. It contains methods to load various frames that
show weather information. It has a method to initialize the application's window as well as a method to kickstart
the main application loop where the GUI starts functioning.

Attributes:
    celsius: A variable to store the weather temperature in Celsius.
    fahrenheit: A variable to store the weather temperature in Fahrenheit.
    weather_description: A string to store the description of the weather.
    cloud_label: Label object to display an image of a cloud in the GUI.
    tk_cloud_image: TKImage object of a cloud.
    cloud_image: Image object of a cloud.
    temperature_frame: Frame object to display temperature information.
    description_frame: Frame object to display weather description.
    main_menu_button: Button object to navigate to the main menu of the application.
    first_frame: Frame object to take city input from the user and display weather data.
    window: Main application window where all frames, labels, and buttons are placed and displayed.
    title_var: Variable to store the title name.
    title: Label object to display title.
    logo: Image object of the application logo.
    tklogo: TKImage object of the application logo.
    logolabel: Label object to display the logo on the main window.
"""


class WeatherApp:
    # Weather API Functions

    def __init__(self):
        # Initialize the main application window
        self.celsius = None
        self.fahrenheit = None
        self.weather_description = None
        self.cloud_label = None
        self.tk_cloud_image = None
        self.cloud_image = None
        self.temperature_frame = None
        self.description_frame = None
        self.main_menu_button = None
        self.first_frame = None
        self.window = ttk.Window(themename="morph")
        self.window.title("weather-app")
        self.window.geometry("600x400")
        self.window.configure(bg="lightblue")
        self.window.resizable(False, False)

        # Title
        self.title_var = ttk.Variable(value="Weather")
        self.title = ttk.Label(self.window, textvariable=self.title_var, font="Calibri 30 bold")
        self.title.configure(background="lightblue")
        self.title.pack()

        # Logo
        self.logo = Image.open("logo.png")
        self.tklogo = ImageTk.PhotoImage(self.logo)
        self.logolabel = ttk.Label(master=self.window, image=self.tklogo)
        self.logolabel.image = self.tklogo
        self.logolabel.configure(background="lightblue")
        self.logolabel.place(x=0, y=0)

        # Load the initial frame for city input
        self.load_first_frame()

    # City Input Frame
    """load_first_frame is a method of the WeatherApp class. It is responsible for creating the initial layout of the
    application, specifically the frame used for the city input search functionality. It defines functions that
    handle various events such as clicking on the search button, entering a city name, and pressing ENTER to trigger
    the search button event. The function also sets design properties such as background color and placement in the
    initial frame."""

    def load_first_frame(self):
        # Create the first frame for city input
        self.first_frame = tk.Frame(master=self.window)

        # Search Button Function
        """Function search_button_func is responsible for the logic behind the search button in the application. This
        function tries to get the input from city_entry_var which is assumed to be the name of a city. If the
        city_entry_var is empty (no input was given), it shows an error message stating "The City You Are Trying To
        Search Is Invalid".

        If a valid city name is present, it calls the function get_weather_data and assigns its return value to class
        variables city_name, weather_description, fahrenheit, and celsius.

        After that, it updates the title_var, hides the first_frame, and loads the second frame via the function
        load_second_frame. If the function completes successfully, it returns True.

        In the case of an exception (for example, if the city provided does not exist or the API fails to fetch
        weather data), it shows the same error message as before and returns False."""

        def search_button_func():
            try:
                City = city_entry_var.get()
                if not City:
                    messagebox.showerror(title="Invalid City", message="The City You Are Trying To Search Is Invalid")
                else:
                    self.city_name, self.weather_description, self.fahrenheit, self.celsius = get_weather_data(
                        City)
                    self.first_frame.place_forget()
                    self.title_var.set(f"{City.title()} Weather")
                    self.load_second_frame()
                    return True
            except Exception:
                tk.messagebox.showerror(title="Invalid City", message="The City You Are Trying To Search Is Invalid")
                return False

        # City Entry Field
        city_entry_var = tk.Variable(value="Enter City...")
        city_entry = ttk.Entry(master=self.first_frame, textvariable=city_entry_var, font="Calibri 20 bold")
        city_entry.configure(width=15)
        city_entry.bind('<FocusIn>', lambda event: on_entry_click(city_entry_var))

        # Search Button
        search_button = ttk.Button(master=self.first_frame, text="Search", command=search_button_func)

        # Pressing ENTER triggers the button event
        """The 'trigger' function acts as an event handler when keys are pressed in the 'city_entry' text field. If
        the 'Return' key is pressed, it calls the 'search_button_func' function, triggering the search for the
        entered city's weather data."""

        def trigger(event):
            if event.keysym == "Return":
                search_button_func()

        city_entry.bind("<KeyPress>", trigger)
        city_entry.pack()
        search_button.pack(padx=10, pady=10)
        self.first_frame.configure(background="lightblue")
        self.first_frame.place(x=190, y=150)

        # Entry Delete Event The 'on_entry_click' function is a callback event bound to the 'FocusIn' event of the
        # city input field within the 'load_first_frame' function. Its main role is to check if the current value of
        # the city input field is equal to the default text 'Enter City...'. If it is, this implies the field hasn't
        # been edited yet by the user. As a response to the focus event (i.e., when the user clicks the field to type
        # in a city name), 'on_entry_click' clears the default text, preparing the field for the user's input.

        def on_entry_click(entry_var):
            # Check if the current value is equal to the placeholder text
            if entry_var.get() == "Enter City...":
                # Delete the current text
                entry_var.set("")

    """
    load_second_frame Function

    This is a method of the WeatherApp class. This function is responsible for loading the second frame in the
    application's user interface (UI). This frame displays weather information as well as a main menu button.

    The method generates and configures several GUI elements including:
        - Main Menu Button: Allows user to navigate back to the main menu.
        - Description frame: Displays the weather description.
        - Temperature frame: Shows information about the temperature in Celsius and Fahrenheit.
        - Cloud Label: Presents a cloud image.

    The main menu button and each frame are placed at specific coordinates on the application's window. After the
    creation of each GUI element, the widget's attributes (like background color, font, text, etc.) are set according
    to the requirements.

    This method does not take any parameters or return any values.
    """

    def load_second_frame(self):
        """
        main_menu_button_func Method

        This is a method within the load_second_frame function that is part of the WeatherApp class. It is
        responsible for the functionality of the main menu button that appears on the weather information display.
        When this button is clicked, it hides the current weather information frames (temperature frame, description
        frame, cloud image), resets the title of the application to its default state, and loads the first frame (
        which allows for city input). This effectively returns the user to the main menu.

        This method does not accept any parameters nor does it return any values. The actions are performed within
        the function itself.
        """

        def main_menu_button_func():
            # Go back to the main menu, hiding the current information frames
            self.description_frame.place_forget()
            self.temperature_frame.place_forget()
            self.cloud_label.forget()
            self.main_menu_button.place_forget()
            self.title_var.set("Weather")
            self.load_first_frame()

        # Create the main menu button
        self.main_menu_button = ttk.Button(master=self.window, text="Main Menu", command=main_menu_button_func)
        self.main_menu_button.place(x=510, y=0)

        # Weather Description Frame
        self.description_frame = tk.Frame(master=self.window)
        weather_desc = ttk.Label(master=self.description_frame, text="Weather Description:", font="Calibri 20 bold")
        weather_desc_info = ttk.Label(master=self.description_frame, text=self.weather_description,
                                      font="Calibri 20 bold")
        weather_desc.configure(background="lightblue")
        weather_desc_info.configure(background="lightblue")
        weather_desc.pack()
        weather_desc_info.pack()
        self.description_frame.configure(background="lightblue")

        # Temperature Frame
        self.temperature_frame = tk.Frame(master=self.window)
        temperature_label = ttk.Label(master=self.temperature_frame, text="Temperature:", font="Calibri 20 bold")
        fahrenheit_info = ttk.Label(master=self.temperature_frame, text=self.fahrenheit, font="Calibri 20 bold")
        celsius_info = ttk.Label(master=self.temperature_frame, text=self.celsius, font="Calibri 20 bold")
        temperature_label.configure(background="lightblue")
        fahrenheit_info.configure(background="lightblue")
        celsius_info.configure(background="lightblue")
        temperature_label.pack()
        fahrenheit_info.pack()
        celsius_info.pack()
        self.temperature_frame.configure(background="lightblue")

        # Cloud Image
        self.cloud_image = Image.open("cloud.png")
        self.tk_cloud_image = ImageTk.PhotoImage(self.cloud_image)
        self.cloud_label = ttk.Label(master=self.window, image=self.tk_cloud_image)
        self.cloud_label.image = self.tk_cloud_image
        self.cloud_label.configure(background="lightblue")
        self.cloud_label.pack(padx=120, pady=10)
        self.temperature_frame.place(x=350, y=300)
        self.description_frame.place(x=50, y=300)

    def run(self):
        # Run the main application loop
        self.window.mainloop()


# Application entry point
if __name__ == '__main__':
    app = WeatherApp()
    app.run()
