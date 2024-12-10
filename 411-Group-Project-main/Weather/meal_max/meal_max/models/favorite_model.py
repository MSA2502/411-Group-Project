import logging
from typing import List
from meal_max.models.kitchen_model import Meal, update_meal_stats
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
        self.favorites: List[Meal] = []

    ##################################################
    # Favorite Management Functions
    ##################################################

    def add_to_favorites(self, meal: Meal) -> None:
        """
        Adds a meal to the favorites list.

        Args:
            meal (Meal): The meal to add to the favorites list.
        
        Raises:
            ValueError: If the meal is already in the favorites list.
        """
        if meal in self.favorites:
            logger.error("Attempted to add '%s' to favorites, but it is already in the list.", meal.meal)
            raise ValueError("This meal is already in your favorites list.")

        # Log the addition of the meal to favorites
        logger.info("Adding '%s' to favorites list", meal.meal)
        self.favorites.append(meal)

        # Log the current state of the favorites list
        logger.info("Current favorites list: %s", [favorite.meal for favorite in self.favorites])

    def remove_from_favorites(self, meal: Meal) -> None:
        """
        Removes a meal from the favorites list.

        Args:
            meal (Meal): The meal to remove from the favorites list.
        
        Raises:
            ValueError: If the meal is not found in the favorites list.
        """
        if meal not in self.favorites:
            logger.error("Attempted to remove '%s' from favorites, but it is not in the list.", meal.meal)
            raise ValueError("This meal is not in your favorites list.")

        # Log the removal of the meal from favorites
        logger.info("Removing '%s' from favorites list", meal.meal)
        self.favorites.remove(meal)

        # Log the current state of the favorites list
        logger.info("Current favorites list: %s", [favorite.meal for favorite in self.favorites])

    def clear_favorites(self) -> None:
        """
        Clears all meals from the favorites list.
        """
        logger.info("Clearing the favorites list.")
        self.favorites.clear()

    def get_favorites(self) -> List[Meal]:
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

    def update_favorite_stats(self, meal_id: int, action: str) -> None:
        """
        Updates the statistics of a favorite meal (e.g., number of times added or removed).
        
        Args:
            meal_id (int): The ID of the meal to update.
            action (str): The action being performed ('add' or 'remove').
        """
        logger.info("Updating stats for meal ID %d with action: %s", meal_id, action)

        # Update stats based on action
        if action == 'add':
            update_meal_stats(meal_id, 'favorite_add')
        elif action == 'remove':
            update_meal_stats(meal_id, 'favorite_remove')
        else:
            logger.error("Invalid action: '%s'. Expected 'add' or 'remove'.", action)

