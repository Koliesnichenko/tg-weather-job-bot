![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-db-blue?logo=postgresql&logoColor=white)
![Railway](https://img.shields.io/badge/Hosted_on-Railway-purple?logo=railway&logoColor=white)
![Status](https://img.shields.io/badge/Version-v1.0-green)
![WIP](https://img.shields.io/badge/WIP-/find%20Command-orange)

# Weather & Job Search Telegram Bot

🚀 [Try the bot on Telegram](https://t.me/JobWeather_bot)  

A multifunctional Telegram bot built with Python that provides:

- 🌤 Real-time weather updates
- 📅 3-day weather forecasts
- 💼 Python job scraping from [python.org](https://python.org/jobs) and [Djinni](https://djinni.co)
- 📍 Location-based forecast via coordinates
- 🔍 Custom job search command: `/find python`, `/find junior remote` (currently disabled in production)

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
  - 🟦 [python.org/jobs](https://python.org/jobs) — *works in production*
  - 🟨 [Djinni.co](https://djinni.co) — *disabled on production (uses Selenium, not supported on Render)*

### 🔍 `/find <keyword>` (Custom Search)
```bash
- Lets users search jobs by keyword  
- Examples: `/find python`, `/find junior remote`  
- ⚠️ Works **locally**, disabled **in production** for now
```
⚠️ Currently disabled in production due to Selenium not being supported on Render.

Placeholder in production

## **Tech Stack**
  ● **python-telegram-bot**
  
  ● **Selenium + BeautifulSoup**
  
  ● **PostgreSQL for user profiles**
  
  ● **.env for secret management**
  
  ● **`Docker` — containerized**
  
  ● **☁️ Hosted on [Render.com](https://render.com)**
  
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
  Selenium is not supported on Render
  Djinni scraping and /find command require Selenium, so they’re disabled in production.
  
  ✅ Works perfectly locally with full job search support.
  🔁 Future versions will migrate from Selenium to requests + BeautifulSoup for full compatibility with cloud hosting.


## Deployment Status
    ● Dockerized
  
    ● Render deployment
  
    ● PostgreSQL connected
  
    ● Weather + /start + buttons work
  
    ● /find to be rewritten without Selenium
