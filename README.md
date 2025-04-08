# ☁️ Weather & Job Search Telegram Bot

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