from dataclasses import dataclass
import logging
import os
import sqlite3
from typing import Any

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


def create_location(location: str) -> None:
    """
    Creates a location object that holds  

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
                INSERT INTO location (location)
                VALUES (?, ?, ?, ?)
            """, (location))
            conn.commit()

            logger.info("Meal successfully added to the database: %s", location)

    except sqlite3.IntegrityError:
        logger.error("Duplicate meal name: %s", location)
        raise ValueError(f"Meal with name '{location}' already exists")

    except sqlite3.Error as e:
        logger.error("Database error: %s", str(e))
        raise e

def clear_locations() -> None:
    """
    Recreates the meals table, effectively deleting all meals.

    Raises:
        sqlite3.Error: If any database error occurs.
    """
    try:
        with open(os.getenv("SQL_CREATE_TABLE_PATH", "/app/sql/create_locarion_table.sql"), "r") as fh:
            create_table_script = fh.read()
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.executescript(create_table_script)
            conn.commit()

            logger.info("Meals cleared successfully.")

    except sqlite3.Error as e:
        logger.error("Database error while clearing meals: %s", str(e))
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
            cursor.execute("SELECT deleted FROM meals WHERE id = ?", (meal_id,))
            try:
                deleted = cursor.fetchone()[0]
                if deleted:
                    logger.info("Meal with ID %s has already been deleted", meal_id)
                    raise ValueError(f"Meal with ID {meal_id} has been deleted")
            except TypeError:
                logger.info("Meal with ID %s not found", meal_id)
                raise ValueError(f"Meal with ID {meal_id} not found")

            cursor.execute("UPDATE meals SET deleted = TRUE WHERE id = ?", (meal_id,))
            conn.commit()

            logger.info("Meal with ID %s marked as deleted.", meal_id)

    except sqlite3.Error as e:
        logger.error("Database error: %s", str(e))
        raise e


def get_weather_for_favorite_locations(location:str) -> None:
    """
    Gets weather for favorite location

    Raises:
        sqlite3.Error: If any database error occurs.
    """
    
api_key = os.getenv("api_key")
base_url = "https://api.openweathermap.org/data/2.5/weather"
city = "Boston"
units = "metric"  # Use "imperial" for Fahrenheit

# Build the URL
params = {
    "q": city,
    "appid": os.getenv(api_key),
    "units": units
}

# Make the API call
response = requests.get(base_url, params=params)

if response.status_code == 200:
    # Parse JSON response
    data = response.json()
    
    # Write the response to a JSON file
    with open("weather_data.json", "w") as json_file:
        json.dump(data, json_file, indent=4)  # indent=4 makes it more readable
    
    print("Data written to 'weather_data.json'")
else:
    print(f"Failed to fetch data: {response.status_code}, {response.text}")

    
def view_all_favorites_with_current_weather() -> None:
    """
    Recreates the meals table, effectively deleting all meals.

    Raises:
        sqlite3.Error: If any database error occurs.
    """
    try:
        with open(os.getenv("SQL_CREATE_TABLE_PATH", "/app/sql/create_meal_table.sql"), "r") as fh:
            create_table_script = fh.read()
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.executescript(create_table_script)
            conn.commit()

            logger.info("Meals cleared successfully.")

    except sqlite3.Error as e:
        logger.error("Database error while clearing meals: %s", str(e))
        raise e

def get_all_favorites(self) -> List[Song]:
        """
        Returns a list of all songs in the playlist.
        """
        self.check_if_empty()
        logger.info("Getting all songs in the playlist")
        return self.playlist


def get_forecast_for_favorite_location() -> None:
    """
    Recreates the meals table, effectively deleting all meals.

    Raises:
        sqlite3.Error: If any database error occurs.
    """
    try:
        with open(os.getenv("SQL_CREATE_TABLE_PATH", "/app/sql/create_meal_table.sql"), "r") as fh:
            create_table_script = fh.read()
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.executescript(create_table_script)
            conn.commit()

            logger.info("Meals cleared successfully.")

    except sqlite3.Error as e:
        logger.error("Database error while clearing meals: %s", str(e))
        raise e