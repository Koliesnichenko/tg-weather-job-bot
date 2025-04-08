![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-db-blue?logo=postgresql&logoColor=white)
![Railway](https://img.shields.io/badge/Hosted_on-Railway-purple?logo=railway&logoColor=white)
![Status](https://img.shields.io/badge/Version-v1.0-green)
![WIP](https://img.shields.io/badge/WIP-/find%20Command-orange)

# Weather & Job Search Telegram Bot

A multifunctional Telegram bot built with Python that provides:

- 🌤 Real-time weather updates
- 📅 3-day weather forecasts
- 💼 Python job scraping from [python.org](https://python.org/jobs) and [Djinni](https://djinni.co)
- 📍 Location-based forecast via coordinates
- 🔍 (WIP) Custom job search command: `/find python`, `/find junior remote`

---

## 🚀 Features

### 🌤 Weather Forecasts
- Uses **OpenWeatherMap API** to get current weather by city or location.
- Forecast view includes temperature, feels like, and sky description.

### 📍 Location Support
- Users can share their geolocation to get local weather conditions.
- Automatically fetches city name from coordinates.

### 💼 Job Fetcher
- Shows recent **Python/Django/Backend** jobs from:
  - 🟦 [python.org/jobs](https://python.org/jobs)
  - 🟨 [Djinni.co](https://djinni.co) — *temporarily limited*

### 🔍 `/find <keyword>` (Custom Search)
```bash
/find python
/find junior remote
```
⚠️ Currently disabled in production due to Selenium not being supported on Railway.

A placeholder is added for now.
Version 2 will use Docker-based deployment on Render to restore full /find functionality.

## **Tech Stack**
  ● **python-telegram-bot**
  
  ● **Selenium + BeautifulSoup**
  
  ● **PostgreSQL for user profiles**
  
  ● **.env for secret management**
  
  ● **Hosted: Railway.app**
  
## PostgreSQL Structure
```
CREATE TABLE users (
    user_id BIGINT PRIMARY KEY,
    name TEXT,
    city TEXT,
    weather_requests INT DEFAULT 0
);
```

## Commands
  ● Command	Description
  ● /start	Welcome message and menu
  ● /location	Share current location
  ● /find <keywords>	🔍 Custom job search (currently disabled on Railway)
  ● Inline Buttons	🌤 Today / 📅 3-day / 💼 Jobs / 👤 Profile / 📍 Set City
  

## Limitations
  Selenium does not run on Railway due to lack of browser support.
  
  /find is disabled on deployed version, but works fine locally.
  
  ✅ Docker + Render deployment is planned to re-enable it in v2.
