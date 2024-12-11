import unittest
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

class TestLocationModel(unittest.TestCase):

    def setUp(self):
        """Setup mock database connection and environment variables."""
        self.mock_conn = MagicMock()
        self.mock_cursor = MagicMock()
        self.mock_conn.cursor.return_value = self.mock_cursor
        patcher = patch('meal_max.utils.sql_utils.get_db_connection', return_value=self.mock_conn)
        self.addCleanup(patcher.stop)
        self.mock_get_db_connection = patcher.start()

        patch_env = patch.dict('os.environ', {'api_key': 'mock_api_key'})
        self.addCleanup(patch_env.stop)
        patch_env.start()

    def tearDown(self):
        """Cleanup after tests."""
        self.mock_conn.reset_mock()
        self.mock_cursor.reset_mock()

    def test_create_location_valid(self):
        """Test creating a valid location."""
        create_location("New York", True, "Sunny", "Cloudy")
        self.mock_cursor.execute.assert_called_once()
        self.mock_conn.commit.assert_called_once()

    def test_create_location_invalid(self):
        """Test creating a location with invalid data."""
        with self.assertRaises(ValueError):
            create_location(123, True, "Sunny", "Cloudy")

    def test_clear_locations(self):
        """Test clearing all locations."""
        clear_locations()
        self.mock_cursor.executescript.assert_called_once()
        self.mock_conn.commit.assert_called_once()

    def test_delete_location_valid(self):
        """Test deleting a valid location."""
        self.mock_cursor.fetchone.return_value = [False]
        delete_location(1)
        self.mock_cursor.execute.assert_any_call("UPDATE location SET deleted = TRUE WHERE id = ?", (1,))
        self.mock_conn.commit.assert_called_once()

    def test_delete_location_not_found(self):
        """Test deleting a location that does not exist."""
        self.mock_cursor.fetchone.return_value = None
        with self.assertRaises(ValueError):
            delete_location(1)

    @patch('requests.get')
    def test_get_weather_for_favorite_location_valid(self, mock_get):
        """Test fetching weather for a favorite location."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "main": {"temp": 20, "humidity": 50},
            "wind": {"speed": 5},
            "weather": [{"description": "clear sky"}]
        }
        mock_get.return_value = mock_response

        result = get_weather_for_favorite_location("New York")
        self.assertEqual(result["temperature"], 20)

    @patch('requests.get')
    def test_get_weather_for_favorite_location_invalid(self, mock_get):
        """Test fetching weather for an invalid location."""
        mock_get.side_effect = requests.RequestException("Invalid API request")
        with self.assertRaises(requests.RequestException):
            get_weather_for_favorite_location("InvalidLocation")

    def test_get_location_by_id_valid(self):
        """Test fetching a location by valid ID."""
        self.mock_cursor.fetchone.return_value = (1, "New York", True, "Sunny", "Cloudy", False)
        location = get_location_by_id(1)
        self.assertEqual(location.location, "New York")

    def test_get_location_by_id_deleted(self):
        """Test fetching a location that is marked as deleted."""
        self.mock_cursor.fetchone.return_value = (1, "New York", True, "Sunny", "Cloudy", True)
        with self.assertRaises(ValueError):
            get_location_by_id(1)

    def test_get_location_by_name_valid(self):
        """Test fetching a location by valid name."""
        self.mock_cursor.fetchone.return_value = (1, "New York", True, "Sunny", "Cloudy", False)
        location = get_location_by_name("New York")
        self.assertEqual(location.location, "New York")

    def test_get_location_by_name_deleted(self):
        """Test fetching a location by name when it is marked as deleted."""
        self.mock_cursor.fetchone.return_value = (1, "New York", True, "Sunny", "Cloudy", True)
        with self.assertRaises(ValueError):
            get_location_by_name("New York")


if __name__ == "__main__":
    unittest.main()
