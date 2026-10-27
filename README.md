# Weather Cache

A small Python script that fetches current weather for a list of cities
using the Open-Meteo API and caches results in SQLite.

## How it works
- Reads city names from cities.txt
- Checks weather.db before calling the API
- Fetches weather only for new cities
- Stores temperature, humidity, and description

## How to run
python weather_cache.py

## Note
Run it twice — the second run uses the database cache instead of the API.
