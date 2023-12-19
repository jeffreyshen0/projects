from tkinter import *
from tkinter import messagebox
from configparser import ConfigParser
import PIL.Image
import PIL.ImageTk
import requests

url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)
api_key = config['api_key']['key']


# retrieving the information from the given json in a formatted manner


def get_weather(city):
    result = requests.get(url.format(city, api_key))
    if result:
        json = result.json()

        city = json['name']
        country = json['sys']['country']
        temp_kelvin = json['main']['temp']
        temp_celsius = temp_kelvin - 273.15
        temp_fahrenheit = (temp_kelvin - 273.15) * 9 / 5 + 32
        icon = json['weather'][0]['icon']
        weather = json['weather'][0]['main']
        description = json['weather'][0]['description']
        min_temp_kelvin = json['main']['temp_min']
        min_temp_celsius = min_temp_kelvin - 273.15
        min_temp_fahrenheit = (min_temp_kelvin - 273.15) * 9 / 5 + 32
        max_temp_kelvin = json['main']['temp_max']
        max_temp_celsius = max_temp_kelvin - 273.15
        max_temp_fahrenheit = (max_temp_kelvin - 273.15) * 9 / 5 + 32
        visibility = json['visibility']
        wind_speed_meters_per_second = json['wind']['speed']
        wind_speed_kilometers_per_hour = wind_speed_meters_per_second * 3.6
        final = (city, country, temp_celsius, temp_fahrenheit, icon,
                 weather, min_temp_celsius, min_temp_fahrenheit,
                 max_temp_celsius, max_temp_fahrenheit, description,
                 visibility, wind_speed_kilometers_per_hour)
        return final

    else:
        return None


# search function
def search():
    global weather_icon
    city = city_text.get()
    weather = get_weather(city)
    if weather:
        location_text['text'] = '{}, {}'.format(weather[0], weather[1])

        im = PIL.Image.open('weather_icons/{}.png'.format(weather[4]))
        render = PIL.ImageTk.PhotoImage(im)

        weather_icon['image'] = render
        weather_icon.image_ref = render
        temperature_label['text'] = \
            ('The current temperature is: {:.2f}°C, {:.2f}°F'.
             format(weather[2], weather[3]))

        weather_label['text'] = weather[5]
        minimum_temp['text'] = (' Low of {:.2f}°C, {:.2f}°F'.
                                format(weather[6], weather[7]))
        maximum_temp['text'] = ('High of {:.2f}°C, {:.2f}°F'.
                                format(weather[8], weather[9]))
        weather_description['text'] = weather[10]
        weather_visibility['text'] = ('The current visibility is {:} meters '.
                                      format(weather[11]))
        current_wind_speed['text'] = ('The wind speed is {:.1f} km/h'.
                                      format(weather[12]))
    else:
        messagebox.showerror('Error', 'Cannot find the city {}'.format(city))


app = Tk()

# configuration of the window

app.title("The Weather App")
app.geometry('700x400')

city_text = StringVar()

# enter and display the city
city_entry = Entry(app, textvariable=city_text)

city_entry.pack()

# search button

city_weather_search_button = Button(app, text='Search Weather',
                                    width=12, command=search)
city_weather_search_button.pack()

# all the labels which appear when a query is entered

location_text = Label(app, text='', font=('bold', 21))
location_text.pack()

load = PIL.Image.open('weather_icons/01d.png')
render = PIL.ImageTk.PhotoImage(load)

weather_icon = Label(app, bitmap='')
weather_icon.pack()

weather_label = Label(app, text='')
weather_label.pack()

temperature_label = Label(app, text='')
temperature_label.pack()

weather_description = Label(app, text='')
weather_description.pack()

minimum_temp = Label(app, text='')
minimum_temp.pack()

maximum_temp = Label(app, text='')
maximum_temp.pack()

weather_visibility = Label(app, text='')
weather_visibility.pack()

current_wind_speed = Label(app, text='')
current_wind_speed.pack()

app.mainloop()
