import datetime
from config import WEATHER_API_KEY
import requests


def get_three_day_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&cnt=24&appid={WEATHER_API_KEY}&units=metric&lang=en"
    response = requests.get(url)
    data = response.json()

    if data.get("cod") != "200":
        return "⚠️ Failed to fetch 3-day forecast."

    result = f"📅 3-Day Forecast for {city.capitalize()}:\n\n"
    seen_dates = set()

    for item in data["list"]:
        date_txt = item["dt_txt"].split(" ")[0]
        if date_txt not in seen_dates:
            seen_dates.add(date_txt)
            temp = item["main"]["temp"]
            desc = item["weather"][0]["description"]
            date_obj = datetime.datetime.strptime(date_txt, "%Y-%m-%d")
            result += f"📆 {date_obj.strftime('%A, %d %b')} — 🌤 {desc.capitalize()}, 🌡 {temp:.1f}°C\n"

        if len(data["list"]) == 3:
            break
    return result
