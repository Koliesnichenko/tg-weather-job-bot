import logging

import requests
from config import WEATHER_API_KEY


def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=en"
    try:
        response = requests.get(url)
        data = response.json()
    except Exception as e:
        logging.error(f"Weather API failed: {e}")
        return "🚫 Failed to fetch weather data."

    if data.get("cod") != 200:
        return "We got weather error."

    temp = data["main"]["temp"]
    feels = data["main"]["feels_like"]
    desc = data["weather"][0]["description"]

    return f"🌤 {city}\nTemperature: {temp}°C\nFeels Like: {feels}°C\n⛅ State: {desc.capitalize()}"


def get_weather_by_coords(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric&lang=en"
    response = requests.get(url)
    data = response.json()

    if data.get("cod") != 200:
        return "🌍 Error on getting weather."

    city = data.get("name", "Unknown")
    temp = data["main"]["temp"]
    feels = data["main"]["feels_like"]
    desc = data["weather"][0]["description"]

    return f"🌤 {city}\n🌡 Temperature: {temp}°C\n🙆‍♂️ Feels Like: {feels}°C\n⛅ State: {desc.capitalize()}"
