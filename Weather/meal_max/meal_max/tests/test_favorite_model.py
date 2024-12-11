import pytest
from meal_max.models.location_model import Location
from meal_max.models.favorite_model import FavoriteModel


@pytest.fixture()
def favorite_model():
    """Fixture to provide a new instance of FavoriteModel for each test."""
    return FavoriteModel()


@pytest.fixture()
def sample_location1():
    """Fixture to provide a sample Location object."""
    return Location(1, "Location 1", True, "Sunny", "Rainy")
#ocation: str, favorite: bool, current_weather: str, forecasted_weather: str


@pytest.fixture()
def sample_location2():
    """Fixture to provide another sample Location object."""
    return Location(2,'Location 2', True, "Snowing", "Tropical")


@pytest.fixture()
def sample_location3():
    """Fixture to provide another sample Location object."""
    return Location(3,'Location 3', True, "Windy", "Chilly")


##################################################
# Add to Favorites Test Cases
##################################################

def test_add_to_favorites(favorite_model, sample_location1):
    """Test adding a location to the favorites."""
    favorite_model.add_to_favorites(sample_location1)
    assert len(favorite_model.favorites) == 1
    assert favorite_model.favorites[0].location == 'Location 1'


def test_add_duplicate_to_favorites(favorite_model, sample_location1):
    """Test adding a duplicate location to the favorites raises a ValueError."""
    favorite_model.add_to_favorites(sample_location1)
    with pytest.raises(ValueError, match="This meal is already in your favorites list."):
        favorite_model.add_to_favorites(sample_location1)


##################################################
# Remove from Favorites Test Cases
##################################################

def test_remove_from_favorites(favorite_model, sample_location1):
    """Test removing a location from the favorites."""
    favorite_model.add_to_favorites(sample_location1)
    favorite_model.remove_from_favorites(sample_location1)
    assert len(favorite_model.favorites) == 0


def test_remove_non_existent_from_favorites(favorite_model, sample_location1):
    """Test removing a location that isn't in the favorites raises a ValueError."""
    with pytest.raises(ValueError, match="This meal is not in your favorites list."):
        favorite_model.remove_from_favorites(sample_location1)


##################################################
# Clear Favorites Test Cases
##################################################

def test_clear_favorites(favorite_model, sample_location1, sample_location2):
    """Test clearing all locations from the favorites list."""
    favorite_model.add_to_favorites(sample_location1)
    favorite_model.add_to_favorites(sample_location2)
    favorite_model.clear_favorites()
    assert len(favorite_model.favorites) == 0


##################################################
# Get Favorites Test Cases
##################################################

def test_get_favorites(favorite_model, sample_location1, sample_location2):
    """Test retrieving the list of favorites."""
    favorite_model.add_to_favorites(sample_location1)
    favorite_model.add_to_favorites(sample_location2)
    favorites = favorite_model.get_favorites()
    assert len(favorites) == 2
    assert favorites[0].location == 'Location 1'
    assert favorites[1].location == 'Location 2'


def test_get_favorite_count(favorite_model, sample_location1, sample_location2):
    """Test getting the count of favorite locations."""
    favorite_model.add_to_favorites(sample_location1)
    favorite_model.add_to_favorites(sample_location2)
    assert favorite_model.get_favorite_count() == 2


##################################################
# Additional Helper Test Cases
##################################################

def test_empty_favorites(favorite_model):
    """Test that the favorites list starts empty."""
    assert len(favorite_model.favorites) == 0


def test_clear_empty_favorites(favorite_model):
    """Test clearing an empty favorites list."""
    favorite_model.clear_favorites()
    assert len(favorite_model.favorites) == 0
