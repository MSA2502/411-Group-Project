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
    location_name = str
    current_weather: str

    def __init__(self):
        """
        Initializes the location model.
        """
        self.id = 1

def create_location(self, location: str) -> dict:
    """
    Creates a location and fetches the weather for that location from the API.

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
            f"Temp: {current_data['main']['temp']}°C, Humidity: {current_data['main']['humidity']}% "
        )
        # Combine and write to JSON file
        weather_result = {
            "id": -1,
            "location": location,
            "current_weather": current_weather
        }

        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO locations(locations, weather)
                    VALUES (?, ?)
                """, (weather_result["location"], weather_result["current_weather"]))
                conn.commit()
                
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM locations WHERE locations = '{location}';")
                tmp = cursor.fetchone()
                weather_result["id"]=tmp[0]
                
                logger.info("Location successfully added to the database: %s", location)
                
        except sqlite3.IntegrityError:
            logger.error("Duplicate location name: %s", location)
            raise ValueError(f"Location with name '{location}' already exists")

        except sqlite3.Error as e:
            logger.error("Database error: %s", str(e))
            raise e

        with open("weather_data.json", "w") as json_file:
            json.dump(weather_result, json_file, indent=4)

        print("Weather data successfully written to 'weather_data.json'")

    except Exception as e:
        print(f"An error occurred while fetching weather data: {e}")
        raise

    return weather_result

def delete_location(location_id: int) -> None:
    """
    Deletes a location using the location_id

    Args:
        location_id(int): the identifier of a location

    Raises:
        sqlite3.Error: If any database error occurs.
        ValueError: if location with location_id can not be found or has been deleted
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

            logger.info("Location cleared successfully.")

    except sqlite3.Error as e:
        logger.error("Database error while clearing locations: %s", str(e))
        raise e

def get_weather_for_location(location_id:int) -> None:
    """
    Gets weather for a favorite location.

    Args:
        location (str): Name of the location to fetch weather for.

    Raises:
        ValueError: If the location is invalid or not a string.
        Exception: If the API call fails or data parsing encounters an error.
    """
    if not isinstance(location_id, int):
        raise ValueError(f"Invalid id: {location_id}. Location_id must be a int.")
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, locations, weather, deleted FROM location WHERE id = ?", (location_id,))
            row = cursor.fetchone()

            if row:
                if row[3]:
                    logger.info("Location with ID %s has been deleted", location_id)
                    raise ValueError(f"Location with ID {location_id} has been deleted")
                return row[2]
            else:
                logger.info("Location with ID %s not found", location_id)
                raise ValueError(f"Location with ID {location_id} not found")

    except sqlite3.Error as e:
        logger.error("Database error: %s", str(e))
        raise e
    
def get_location_by_id(location_id: int) -> None:
    """
    Gets a location by its id
    
    Args:
        location_id(int): unique identifier of a location object
    
    Returns:
        Location object
    
    Raises:
        sqlite3.Error: If any database error occurs.
        ValueError: if location with location_id can not be found or has been deleted
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, locations, weather, deleted FROM location WHERE id = ?", (location_id,))
            row = cursor.fetchone()

            if row:
                if row[3]:
                    logger.info("Location with ID %s has been deleted", location_id)
                    raise ValueError(f"Location with ID {location_id} has been deleted")
                return row[1]
            else:
                logger.info("Location with ID %s not found", location_id)
                raise ValueError(f"Location with ID {location_id} not found")

    except sqlite3.Error as e:
        logger.error("Database error: %s", str(e))
        raise e
