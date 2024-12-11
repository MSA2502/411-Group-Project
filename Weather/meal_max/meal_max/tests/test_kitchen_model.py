from unittest import TestCase, main
from unittest.mock import patch, MagicMock
import sqlite3
import requests
from meal_max.models.location_model import (
    create_location, 
    clear_locations, 
    delete_location, 
    get_weather_for_favorite_location,
    get_forecast_for_favorite_location,
    get_location_by_id,
    get_location_by_name
)

# Setup mock database connection and environment variables
mock_conn = MagicMock()
mock_cursor = MagicMock()
mock_conn.cursor.return_value = mock_cursor
patcher = patch('meal_max.utils.sql_utils.get_db_connection', return_value=mock_conn)
mock_get_db_connection = patcher.start()

patch_env = patch.dict('os.environ', {'api_key': 'mock_api_key'})
patch_env.start()

def tearDownModule():
    """Clean up after tests."""
    patcher.stop()
    patch_env.stop()

# Test creating a valid location
def test_create_location_valid():
    create_location("New York", True, "Sunny", "Cloudy")
    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_called_once()

# Test creating a location with invalid data
def test_create_location_invalid():
    try:
        create_location(123, True, "Sunny", "Cloudy")
    except ValueError as e:
        assert str(e) == "Invalid location: 123. Location must be a string."

# Test clearing all locations
def test_clear_locations():
    clear_locations()
    mock_cursor.executescript.assert_called_once()
    mock_conn.commit.assert_called_once()

# Test deleting a valid location
def test_delete_location_valid():
    mock_cursor.fetchone.return_value = [False]
    delete_location(1)
    mock_cursor.execute.assert_any_call("UPDATE location SET deleted = TRUE WHERE id = ?", (1,))
    mock_conn.commit.assert_called_once()

# Test deleting a location that does not exist
def test_delete_location_not_found():
    mock_cursor.fetchone.return_value = None
    try:
        delete_location(1)
    except ValueError as e:
        assert str(e) == "Location with ID 1 not found"

# Test fetching weather for a favorite location
@patch('requests.get')
def test_get_weather_for_favorite_location_valid(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "main": {"temp": 20, "humidity": 50},
        "wind": {"speed": 5},
        "weather": [{"description": "clear sky"}]
    }
    mock_get.return_value = mock_response

    result = get_weather_for_favorite_location("New York")
    assert result["temperature"] == 20

# Test fetching weather for an invalid location
@patch('requests.get')
def test_get_weather_for_favorite_location_invalid(mock_get):
    mock_get.side_effect = requests.RequestException("Invalid API request")
    try:
        get_weather_for_favorite_location("InvalidLocation")
    except requests.RequestException as e:
        assert str(e) == "Invalid API request"

# Test fetching a location by valid ID
def test_get_location_by_id_valid():
    mock_cursor.fetchone.return_value = (1, "New York", True, "Sunny", "Cloudy", False)
    location = get_location_by_id(1)
    assert location.location == "New York"

# Test fetching a location that is marked as deleted
def test_get_location_by_id_deleted():
    mock_cursor.fetchone.return_value = (1, "New York", True, "Sunny", "Cloudy", True)
    try:
        get_location_by_id(1)
    except ValueError as e:
        assert str(e) == "Location with ID 1 has been deleted"

# Test fetching a location by valid name
def test_get_location_by_name_valid():
    mock_cursor.fetchone.return_value = (1, "New York", True, "Sunny", "Cloudy", False)
    location = get_location_by_name("New York")
    assert location.location == "New York"

# Test fetching a location by name when it is marked as deleted
def test_get_location_by_name_deleted():
    mock_cursor.fetchone.return_value = (1, "New York", True, "Sunny", "Cloudy", True)
    try:
        get_location_by_name("New York")
    except ValueError as e:
        assert str(e) == "Location with name New York has been deleted"

if __name__ == "__main__":
    main()
