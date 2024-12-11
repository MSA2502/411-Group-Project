import pytest
from unittest.mock import patch, MagicMock
from meal_max.utils.sql_utils import get_db_connection
from meal_max.utils.logger import configure_logger
from contextlib import contextmanager

from meal_max.models.location_model import (
    Location,
    create_location,
    clear_locations, 
    delete_location, 
    get_weather_for_location,
    get_location_by_id
    
)
import requests
import sqlite3
import json


@pytest.fixture
def mock_cursor(mocker):
    mock_conn = mocker.Mock()
    mock_cursor = mocker.Mock()

    # Mock the connection's cursor
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None  # Default return for queries
    mock_cursor.fetchall.return_value = []
    mock_conn.commit.return_value = None


    # Mock the get_db_connection context manager from sql_utils
    @contextmanager
    def mock_get_db_connection():
        yield mock_conn  # Yield the mocked connection object
    mocker.patch("meal_max.models.location_model.get_db_connection", mock_get_db_connection)
    return mock_cursor  # Return the mock cursor so we can set expectations per test


@pytest.fixture
def mock_requests():
    """Mock the requests.get function."""
    with patch('requests.get') as mock_get:
        yield mock_get


def test_create_location(mock_requests, mock_cursor):
    """Test create_location function."""
    # Mock the weather API response
    mock_weather_data = {
        'weather': [{'main': 'Clear', 'description': 'clear sky'}],
        'main': {'temp': 25, 'humidity': 60}
    }
    mock_requests.return_value.status_code = 200
    mock_requests.return_value.json.return_value = mock_weather_data


    location = Location()

    # Call the function to test
    result = create_location("Test City")

    # Verify that the result is correct
    assert result['location'] == 'Test City'
    assert "Temp: 25°C" in result['current_weather']

    # Verify the database interaction
    mock_db_connection.execute.assert_called_with("""
        INSERT INTO locations(locations, weather)
        VALUES (?, ?)
    """, ('Test City', 'Clear (clear sky), Temp: 25°C, Humidity: 60%'))


def test_create_location_invalid_location(mock_db_connection):
    """Test create_location when an invalid location (non-string) is passed."""
    location = Location()

    with pytest.raises(ValueError, match="Invalid location: 123. Location must be a string."):
        location.create_location(123)  # Invalid location


def test_delete_location(mock_db_connection):
    """Test delete_location function."""
    mock_db_connection.fetchone.return_value = (False,)
    mock_db_connection.execute.return_value = None

    # Call delete_location
    delete_location(1)

    # Verify the correct SQL query was executed
    mock_db_connection.execute.assert_called_with("UPDATE location SET deleted = TRUE WHERE id = ?", (1,))


def test_delete_location_not_found(mock_db_connection):
    """Test delete_location when location is not found."""
    mock_db_connection.fetchone.return_value = None

    with pytest.raises(ValueError, match="Location with ID 1 not found"):
        delete_location(1)


def test_get_weather_for_location(mock_db_connection):
    """Test get_weather_for_location function."""
    mock_db_connection.fetchone.return_value = (1, 'Test City', 'Clear (clear sky), Temp: 25°C, Humidity: 60%', False)

    # Call get_weather_for_location
    weather = get_weather_for_location(1)

    # Verify the result
    assert weather == 'Clear (clear sky), Temp: 25°C, Humidity: 60%'


def test_get_weather_for_location_deleted(mock_db_connection):
    """Test get_weather_for_location when the location is marked as deleted."""
    mock_db_connection.fetchone.return_value = (1, 'Test City', 'Clear (clear sky), Temp: 25°C, Humidity: 60%', True)

    with pytest.raises(ValueError, match="Location with ID 1 has been deleted"):
        get_weather_for_location(1)


def test_get_location_by_id(mock_db_connection):
    """Test get_location_by_id function."""
    mock_db_connection.fetchone.return_value = (1, 'Test City', 'Clear (clear sky), Temp: 25°C, Humidity: 60%', False)

    # Call get_location_by_id
    location = get_location_by_id(1)

    # Verify the result
    assert location == 'Test City'


def test_get_location_by_id_not_found(mock_db_connection):
    """Test get_location_by_id when the location is not found."""
    mock_db_connection.fetchone.return_value = None

    with pytest.raises(ValueError, match="Location with ID 1 not found"):
        get_location_by_id(1)