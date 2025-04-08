import requests
from collections import defaultdict
from datetime import datetime
from config import WEATHER_API_KEY


def get_three_day_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=en"
    response = requests.get(url)
    data = response.json()

    if data.get("cod") != "200":
        return "⚠️ Failed to fetch 3-day forecast."

    grouped = defaultdict(list)

    for entry in data["list"]:
        date = entry["dt_txt"].split(" ")[0]  # YYYY-MM-DD
        grouped[date].append(entry)

    result = f"📅 3-Day Forecast for {city.capitalize()}:\n\n"
    count = 0

    for date, forecasts in grouped.items():
        if count == 3:
            break

        midday = min(forecasts, key=lambda x: abs(int(x["dt_txt"].split()[1][:2]) - 12))
        desc = midday["weather"][0]["description"].capitalize()
        temp = midday["main"]["temp"]
        readable_date = datetime.strptime(date, "%Y-%m-%d").strftime("%A, %d %b")
        result += f"📆 {readable_date} — 🌤 {desc}, 🌡 {temp:.1f}°C\n"
        count += 1

    return result
