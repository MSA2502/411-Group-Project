from dataclasses import dataclass
import logging
import os
import sqlite3
from typing import Any

import logging
from typing import List

from meal_max.utils.sql_utils import get_db_connection
from meal_max.utils.logger import configure_logger

import requests
import json
from dotenv import load_dotenv
import os




load_dotenv()
logger = logging.getLogger(__name__)
configure_logger(logger)


@dataclass
class Location:
    id: int
    location: str
    favorite: bool
    current_weather: str
    forecasted_weather: str


    def __post_init__(self):
        if self.location != type(str):
            raise ValueError("location must be a string ")


def create_location(location: str, favorite: bool, current_weather: str, forecasted_weather: str) -> None:
    """
    Creates a location object  

    Args:
        location(str): the location 
        favorite(bool): is the location a favorite or not (determined by True of False statement)
    
     Raises:
        sqlite3.Error: If any database error occurs.
        sqlite3.IntegrityError: if a duplicate meal object already exists
        ValueError: if a meal with the same name exists
    """
    if not isinstance(location, (str)):
        raise ValueError(f"Invalid location: {location}. Location must be a string.")

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO locations(location, weather, favorite, current_weather, forecasted_weather)
                VALUES (?, ?, ?, ?)
            """, (location, favorite, current_weather, forecasted_weather))
            conn.commit()

            logger.info("Location successfully added to the database: %s", location)

    except sqlite3.IntegrityError:
        logger.error("Duplicate location name: %s", location)
        raise ValueError(f"Locatio  with name '{location}' already exists")

    except sqlite3.Error as e:
        logger.error("Database error: %s", str(e))
        raise e

def clear_locations() -> None:
    """
    Recreates the locations table, effectively deleting all locations.

    Raises:
        sqlite3.Error: If any database error occurs.
    """
    try:
        with open(os.getenv("SQL_CREATE_TABLE_PATH", "/app/sql/create_location_table.sql"), "r") as fh:
            create_table_script = fh.read()
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.executescript(create_table_script)
            conn.commit()

            logger.info("Locations cleared successfully.")

    except sqlite3.Error as e:
        logger.error("Database error while clearing locations: %s", str(e))
        raise e

def delete_location(location_id: int) -> None:
    """
    Deletes a location using the location_id

    Args:
        location_id(int): the identifier of a location

    Raises:
        sqlite3.Error: If any database error occurs.
        ValueError: if meal with meal_id can not be found or has been deleted
        TypeError: If any type error occurs
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT deleted FROM locations WHERE id = ?", (location_id,))
            try:
                deleted = cursor.fetchone()[0]
                if deleted:
                    logger.info("Location with ID %s has already been deleted", location_id)
                    raise ValueError(f"Location with ID {location_id} has been deleted")
            except TypeError:
                logger.info("Location with ID %s not found", location_id)
                raise ValueError(f"Location with ID {location_id} not found")

            cursor.execute("UPDATE location SET deleted = TRUE WHERE id = ?", (location_id,))
            conn.commit()

            logger.info("Location with ID %s marked as deleted.", location_id)

    except sqlite3.Error as e:
        logger.error("Database error: %s", str(e))
        raise e




def get_weather_for_favorite_location(location: str) -> dict:
    """
    Fetches current weather for a favorite location.

    Args:
        location (str): The location to fetch weather for.

    Returns:
        dict: Weather details including temperature, humidity, wind speed, and conditions.

    Raises:
        ValueError: If the location is invalid.
        requests.RequestException: For API call issues.
    """
    api_key = os.getenv("api_key")
    if not api_key:
        raise ValueError("API key is missing in the environment variables.")
    
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": location, "appid": api_key, "units": "metric"}

    response = requests.get(base_url, params=params)
    response.raise_for_status()  # Raise an exception for HTTP errors

    weather_data = response.json()
    return {
        "location": location,
        "temperature": weather_data["main"]["temp"],
        "humidity": weather_data["main"]["humidity"],
        "wind_speed": weather_data["wind"]["speed"],
        "conditions": weather_data["weather"][0]["description"]
    }


def get_weather_for_location(location: str) -> None:
    """
    Gets weather for a favorite location, including current and forecasted weather.

    Args:
        location (str): Name of the location to fetch weather for.

    Raises:
        ValueError: If the location is invalid or not a string.
        Exception: If the API call fails or data parsing encounters an error.
    """
    if not isinstance(location, str):
        raise ValueError(f"Invalid location: {location}. Location must be a string.")

    # Load API key and set base URLs
    api_key = os.getenv(api_key)
    if not api_key:
        raise ValueError("API key not found in environment variables.")

    weather_url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": location,
        "appid": api_key,
        "units": "metric"  # Metric units for temperature in Celsius
    }

    try:
        # Get current weather
        current_response = requests.get(weather_url, params=params)
        if current_response.status_code != 200:
            raise Exception(f"Failed to fetch current weather: {current_response.status_code}, {current_response.text}")

        current_data = current_response.json()
        current_weather = (
            f"{current_data['weather'][0]['main']} ({current_data['weather'][0]['description']}), "
            f"Temp: {current_data['main']['temp']}°C, Humidity: {current_data['main']['humidity']}%, "
            f"Wind: {current_data['wind']['speed']} m/s"
        )

        # Combine and write to JSON file
        weather_result = {
            "location": location,
            "current_weather": current_weather
        }

        with open("weather_data.json", "w") as json_file:
            json.dump(weather_result, json_file, indent=4)

        print("Weather data successfully written to 'weather_data.json'")

    except Exception as e:
        print(f"An error occurred while fetching weather data: {e}")
        raise

def get_forecast_for_favorite_location(location: str) -> None: 
    """
    Gets weather for a favorite location, including current and forecasted weather.

    Args:
        location (str): Name of the location to fetch weather for.

    Raises:
        ValueError: If the location is invalid or not a string.
        Exception: If the API call fails or data parsing encounters an error.
    """
    if not isinstance(location, str):
        raise ValueError(f"Invalid location: {location}. Location must be a string.")

    # Load API key and set base URLs
    api_key = os.getenv(api_key)
    if not api_key:
        raise ValueError("API key not found in environment variables.")

    forecast_url = "https://api.openweathermap.org/data/2.5/forecast"

    params = {
        "q": location,
        "appid": os.getenv(api_key),
        "units": "metric"  # Metric units for temperature in Celsius
    }

    try:
        # Get forecasted weather
        forecast_response = requests.get(forecast_url, params=params)
        if forecast_response.status_code != 200:
            raise Exception(f"Failed to fetch forecasted weather: {forecast_response.status_code}, {forecast_response.text}")

        forecast_data = forecast_response.json()
        forecasted_weather = "\n".join(
            [
                f"{item['dt_txt']}: {item['weather'][0]['description']}, Temp: {item['main']['temp']}°C"
                for item in forecast_data['list'][:3]  # Fetching next three forecast entries (3-hour intervals)
            ]
        )

        # Combine and write to JSON file
        forecast_result = {
            "location": location,
            "forecasted_weather": forecasted_weather
        }

        with open("forecast_data.json", "w") as json_file:
            json.dump(forecast_result, json_file, indent=4)

        print("Weather data successfully written to 'forecast_data.json'")

    except Exception as e:
        print(f"An error occurred while fetching weather data: {e}")
        raise

    
def get_location_by_id(location_id: int) -> Location:
    """
    Gets a meal by its id
    
    Args:
        meal_id(int): unique identifier of a meal object
    
    Returns:
        Location object
    
    Raises:
        sqlite3.Error: If any database error occurs.
        ValueError: if meal with meal_id can not be found or has been deleted
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, location, favorite, weather, forecast, deleted FROM location WHERE id = ?", (location_id,))
            row = cursor.fetchone()

            if row:
                if row[5]:
                    logger.info("Location with ID %s has been deleted", location_id)
                    raise ValueError(f"Location with ID {location_id} has been deleted")
                return Location(id=row[0], location=row[1], favorite=row[2], weather=row[3], forecast=row[4])
            else:
                logger.info("Meal with ID %s not found", location_id)
                raise ValueError(f"Location with ID {location_id} not found")

    except sqlite3.Error as e:
        logger.error("Database error: %s", str(e))
        raise e

def get_location_by_name(location_name: str) -> Location:
    """
    Gets a location by its name
    
    Args:
        location_name(str): the name of a location
    
    Returns:
        returns a Location object
    
    Raises:
        sqlite3.Error: If any database error occurs.
        ValueError: if location with location_name is not found or has been deleted
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, location, favorite, weather, forecast, deleted FROM location WHERE id = ?", (location_name,))
            row = cursor.fetchone()

            if row:
                if row[5]:
                    logger.info("Location with name %s has been deleted", location_name)
                    raise ValueError(f"Location with name {location_name} has been deleted")
                return Location(id=row[0], locations=row[1], cuisine=row[2], price=row[3], difficulty=row[4])
            else:
                logger.info("Location with name %s not found", location_name)
                raise ValueError(f"Location with name {location_name} not found")

    except sqlite3.Error as e:
        logger.error("Database error: %s", str(e))
        raise e


