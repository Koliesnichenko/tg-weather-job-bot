import requests
from config import WEATHER_API_KEY


def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=en"
    response = requests.get(url)
    data = response.json()

    if data.get("cod") != 200:
        return "We got weather error."

    temp = data["main"]["temp"]
    feels = data["main"]["feels_like"]
    desc = data["weather"][0]["description"]

    return f"🌤 {city}\nTemperature: {temp}°C\nFeels Like: {feels}°C\nState: {desc.capitalize()}"
