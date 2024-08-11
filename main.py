import json
import os
import asyncio
from typing import Tuple, Dict
import requests
from database.database import get_data_from_geocoding_db, update_weather_forecasts
from log import logger
from exceptions import CityNotFoundError, DateNotFoundError

API_KEY = os.getenv("OPENWEATHERMAP_API_KEY", "115c2619da26f884b28d4af39340077a")


def get_geocode(city: str = "London") -> Tuple[str, str, float, float] | None:
    """Get geocode data from OpenWeatherMap API."""
    url: str = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching geocode data: {e}")
        return None

    if not data:
        logger.error("No data found for the specified city.")
        return None

    return data[0]["name"], data[0]["country"], data[0]["lat"], data[0]["lon"]


def get_weather(name: str, country: str, lat: float, lon: float) -> Dict | None:
    """Get weather data from OpenWeatherMap API."""
    url: str = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&appid={API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching weather data: {e}")
        return None

    os.makedirs("weather_json", exist_ok=True)
    file_path = os.path.join("weather_json", f"data_weather_{name}.json")

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    return data


def read_weather_json(city: str) -> Dict:
    """Read weather data from JSON file."""
    file_path = os.path.join("weather_json", f"data_weather_{city}.json")
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


async def get_weather_data(city: str, date: str) -> Dict:
    """Get weather data for a specific city and date."""
    city_found = False
    for file in os.listdir("weather_json"):
        if city in file:
            city_found = True
            file_path = os.path.join("weather_json", file)
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                for forecast in data["list"]:
                    if forecast["dt_txt"] == date:
                        return forecast

    if not city_found:
        raise CityNotFoundError(f"City '{city}' not found")

    raise DateNotFoundError(f"No weather data found for date '{date}' in city '{city}'")


async def main():
    cities = ['New York County', 'London', 'Paris', 'Tokyo', 'Istanbul', 'Berlin', 'Rome', 'Moscow', 'Seoul', 'Beijing',
              'Shanghai', 'Bangkok', 'Sydney', 'Cairo', 'Los Angeles', 'Mexico City', 'Buenos Aires', 'Cape Town',
              'Dubai', 'Lagos']

    # Get latitude and longitude and write them to the database
    # for city in cities:
    #     geocode = get_geocode(city)
    #     if geocode:
    #         name, country, lat, lon = geocode
    #         logger.info(name, country, lat, lon)
    #         connect_db(name, country, round(lat, 2), round(lon, 2))

    while True:
        try:
            # Get weather data from OpenWeatherMap
            print('Retrieving weather data from OpenWeatherMap')
            for city in cities:
                name, country, lat, lon = get_data_from_geocoding_db(city)
                if all([name, country, lat, lon]):
                    logger.debug(name, country, lat, lon)
                    weather_data = get_weather(name, country, lat, lon)
                    if weather_data:
                        logger.debug(weather_data)
            print('Retrieved weather data from OpenWeatherMap')
        except Exception as e:
            logger.error(f'An error occurred while retrieving weather from the site: {e}')

        try:
            # Update weather in the database
            for city in cities:
                weather_json = read_weather_json(city)
                result = [(city, forecast['dt_txt'], forecast['main']['temp']) for forecast in weather_json['list']]
                update_weather_forecasts(result)
        except Exception as e:
            logger.error(f'An error occurred while updating the weather in the database: {e}')
        print('Updated weather in the database')
        print('Waiting for an hour...')
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main())
