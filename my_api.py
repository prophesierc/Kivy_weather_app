
import requests
import geocoder
import os

g = geocoder.ip('me')
api_key = os.environ['api_key']

#API request
url = f'https://api.openweathermap.org/data/2.5/weather?lat={g.lat}&lon={g.lng}&appid={api_key}&units=imperial'
response = requests.get(url)
data = response.json()

def weather_temp():
	return f"{round(data['main']['temp'])}°"


def weather_icon():
	current_weather_icon = f"{data['weather'][0]['icon']}"
	img_url = f'http://openweathermap.org/img/wn/{current_weather_icon}@4x.png'
	return img_url

def feels_like():
	return f"{round(data['main']['feels_like'])}°"

def description():
	return f"{data['weather'][0]['description'].title()}"
