import pytest
from unittest.mock import patch, MagicMock
from meal_max.models.location_model import Location, create_location, clear_locations, delete_location, get_weather_for_favorite_locations

@pytest.fixture
def sample_location():
    """Fixture to provide a sample location object."""
    return Location(id=1, location="Boston", favorite=True, current_weather="Sunny", forecasted_weather="Rainy")

##################################################
# Location Object Test Cases
##################################################

def test_location_initialization(sample_location):
    """Test initializing a Location object."""
    assert sample_location.location == "Boston", "Expected location to be 'Boston'"
    assert sample_location.favorite is True, "Expected favorite to be True"
    assert sample_location.current_weather == "Sunny", "Expected current weather to be 'Sunny'"
    assert sample_location.forecasted_weather == "Rainy", "Expected forecasted weather to be 'Rainy'"

def test_location_type_validation():
    """Test invalid type for location raises a ValueError."""
    with pytest.raises(ValueError, match="location must be a string"):
        Location(id=1, location=123, favorite=True, current_weather="Sunny", forecasted_weather="Rainy")

##################################################
# Database Interaction Test Cases
##################################################

@patch("meal_max.utils.sql_utils.get_db_connection", return_value=MagicMock())
def test_create_location(mock_get_db_connection):
    """Test creating a location."""
    mock_cursor = mock_get_db_connection.return_value.cursor.return_value
    create_location("Boston")
    mock_cursor.execute.assert_called_once_with(
        """
        INSERT INTO location (location)
        VALUES (?, ?, ?, ?)
        """,
        ("Boston"),
    )

@patch("meal_max.utils.sql_utils.get_db_connection", return_value=MagicMock())
def test_clear_locations(mock_get_db_connection):
    """Test clearing locations."""
    mock_cursor = mock_get_db_connection.return_value.cursor.return_value
    clear_locations()
    mock_cursor.executescript.assert_called()

@patch("meal_max.utils.sql_utils.get_db_connection", return_value=MagicMock())
def test_delete_location(mock_get_db_connection):
    """Test deleting a location."""
    mock_cursor = mock_get_db_connection.return_value.cursor.return_value
    mock_cursor.fetchone.return_value = [False]
    delete_location(1)
    mock_cursor.execute.assert_called_with("UPDATE locations SET deleted = TRUE WHERE id = ?", (1,))

##################################################
# Weather API Test Cases
##################################################

@patch("requests.get")
def test_get_weather_for_favorite_locations(mock_requests_get):
    """Test fetching weather for favorite locations."""
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = {"weather": "Sunny"}
    result = get_weather_for_favorite_locations("Boston")
    mock_requests_get.assert_called_once()
    assert result is not None, "Expected a response from the API"

##################################################
# Utility Function Test Cases
##################################################

@patch("meal_max.utils.sql_utils.get_db_connection", return_value=MagicMock())
def test_view_all_favorites_with_current_weather(mock_get_db_connection):
    """Test viewing all favorites with current weather."""
    mock_cursor = mock_get_db_connection.return_value.cursor.return_value
    view_all_favorites_with_current_weather()
    mock_cursor.executescript.assert_called()

# Additional tests for forecast and favorites can follow a similar pattern.