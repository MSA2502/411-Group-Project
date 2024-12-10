import logging
from typing import List
from meal_max.models.location_model import Location
from meal_max.utils.logger import configure_logger

logger = logging.getLogger(__name__)
configure_logger(logger)


class FavoriteModel:
    """
    A class to manage the list of favorite meals.

    Attributes:
        favorites (List[Meal]): The current list of favorite meals.
    """

    def __init__(self):
        """
        Initializes the FavoriteModel with an empty favorites list.
        """
        self.favorites: List[Location] = []

    ##################################################
    # Favorite Management Functions
    ##################################################

    def add_to_favorites(self, location: Location) -> None:
        """
        Adds a meal to the favorites list.

        Args:
            meal (Meal): The meal to add to the favorites list.
        
        Raises:
            ValueError: If the meal is already in the favorites list.
        """
        if location in self.favorites:
            logger.error("Attempted to add '%s' to favorites, but it is already in the list.", location.location)
            raise ValueError("This meal is already in your favorites list.")

        # Log the addition of the meal to favorites
        logger.info("Adding '%s' to favorites list", location.location)
        self.favorites.append(location)

        # Log the current state of the favorites list
        logger.info("Current favorites list: %s", [favorite.location for favorite in self.favorites])

    def remove_from_favorites(self, location: Location) -> None:
        """
        Removes a meal from the favorites list.

        Args:
            meal (Meal): The meal to remove from the favorites list.
        
        Raises:
            ValueError: If the meal is not found in the favorites list.
        """
        if location not in self.favorites:
            logger.error("Attempted to remove '%s' from favorites, but it is not in the list.", location.location)
            raise ValueError("This meal is not in your favorites list.")

        # Log the removal of the meal from favorites
        logger.info("Removing '%s' from favorites list", location.location)
        self.favorites.remove(location)

        # Log the current state of the favorites list
        logger.info("Current favorites list: %s", [favorite.location for favorite in self.favorites])

    def clear_favorites(self) -> None:
        """
        Clears all meals from the favorites list.
        """
        logger.info("Clearing the favorites list.")
        self.favorites.clear()

    def get_favorites(self) -> List[Location]:
        """
        Returns the current list of favorite meals.
        """
        logger.info("Retrieving current list of favorites.")
        return self.favorites

    def get_favorite_count(self) -> int:
        """
        Returns the total number of favorite meals.
        """
        logger.info("Retrieving the number of favorites: %d", len(self.favorites))
        return len(self.favorites)

    ##################################################
    # Favorite Meal Statistics
    ##################################################

    # def update_favorite_stats(self, location_id: int, action: str) -> None:
    #     """
    #     Updates the statistics of a favorite meal (e.g., number of times added or removed).
        
    #     Args:
    #         meal_id (int): The ID of the meal to update.
    #         action (str): The action being performed ('add' or 'remove').
    #     """
    #     logger.info("Updating stats for meal ID %d with action: %s", location_id, action)

    #     # Update stats based on action
    #     if action == 'add':
    #         update_meal_stats(location_id, 'favorite_add')
    #     elif action == 'remove':
    #         update_meal_stats(location_id, 'favorite_remove')
    #     else:
    #         logger.error("Invalid action: '%s'. Expected 'add' or 'remove'.", action)

