import ttkbootstrap as ttk
from PIL import Image, ImageTk
import tkinter as tk
import requests
from tkinter import messagebox


"""
The 'WeatherApp' class is the main class implemented for creating a graphical interface for a weather application. This application retrieves weather
data from an API, and the results are presented in the form of a simple GUI (Graphical User Interface).

The class consists of several methods, including:
- 'get_weather_data': This method retrieves the current weather data from the OpenWeatherMap API for a specified city and parses the JSON response to
  extract necessary information like weather description, city name, and temperature.
- 'kelvin_to_celsius_fahrenheit': It converts the temperature value from Kelvin to Celsius and Fahrenheit.
- '__init__': Initializes the object of WeatherApp class, defines the main application window, and calls the 'load_first_frame' method to start the
  application with the city input frame.
- 'load_first_frame': Sets the first frame, which handles the city input and triggers API call and navigation to the second frame on valid input.
- 'load_second_frame': Displays the results from the API call in a second frame.
- 'run': Starts the tkinter mainloop to run the application.

Users interact with the application by typing the name of a city into an input field. The application then retrieves weather data for that city and
displays the information regarding the weather description and temperature in Celsius and Fahrenheit.
"""


class WeatherApp:
    # Weather API Functions
    def get_weather_data(self, city):
        # API request to OpenWeatherMap to get weather data
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city},us&APPID=07b914069d0550579f1980d1c73d8d92"
        response = requests.get(url).json()

        # Extract relevant information from the API response
        weather_description = response["weather"][0]["description"]
        city_name = response["name"]
        kelvin_temperature = response["main"]["temp"]
        celsius, fahrenheit = self.kelvin_to_celsius_fahrenheit(kelvin_temperature)
        celsius = f"{celsius:.0f}C"
        fahrenheit = f"{fahrenheit:.0f}F"
        weather_description = weather_description.title()
        return (city_name, weather_description, fahrenheit, celsius)

    def kelvin_to_celsius_fahrenheit(self, kelvin: int):
        # Convert temperature from Kelvin to Celsius and Fahrenheit
        celsius = kelvin - 273.15
        fahrenheit = celsius * (9 / 5) + 32
        return celsius, fahrenheit

    def __init__(self):
        # Initialize the main application window
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
    def load_first_frame(self):
        # Create the first frame for city input
        self.first_frame = tk.Frame(master=self.window)

        # Search Button Function
        def search_button_func():
            try:
                City = city_entry_var.get()
                if not City:
                    messagebox.showerror(title="Invalid City", message="The City You Are Trying To Search Is Invalid")
                else:
                    self.city_name, self.weather_description, self.fahrenheit, self.celsius = self.get_weather_data(
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
        def trigger(event):
            if event.keysym == "Return":
                search_button_func()

        city_entry.bind("<KeyPress>", trigger)
        city_entry.pack()
        search_button.pack(padx=10, pady=10)
        self.first_frame.configure(background="lightblue")
        self.first_frame.place(x=190, y=150)

        # Entry Delete Event
        def on_entry_click(entry_var):
            # Check if the current value is equal to the placeholder text
            if entry_var.get() == "Enter City...":
                # Delete the current text
                entry_var.set("")

    # Second Frame (info about the given city)
    def load_second_frame(self):
        # Main Menu Button
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
