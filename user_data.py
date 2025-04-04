import json
import os

DATA_FILE = "users.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def set_city(user_id, city, name):
    data = load_data()
    user_id = str(user_id)
    if user_id not in data:
        data[user_id] = {"city": city, "name": name, "weather_requests": 0}
    else:
        data[user_id]["city"] = city
        data[user_id]["name"] = name
    save_data(data)


def get_city(user_id):
    return load_data().get(str(user_id), {}).get("city")


def increment_weather_counter(user_id):
    data = load_data()
    user_id = str(user_id)
    if user_id in data:
        data[user_id]["weather_requests"] = data[user_id].get("weather_requests", 0) + 1
        save_data(data)


def get_profile(user_id):
    return load_data().get(str(user_id), {})


def delete_profile(user_id):
    data = load_data()
    user_id = str(user_id)
    if user_id in data:
        del data[user_id]
        save_data(data)
        return True
    return False
