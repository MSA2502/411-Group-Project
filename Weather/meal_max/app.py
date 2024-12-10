from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, Response, request
# from flask_cors import CORS

from meal_max.models import location_model
from meal_max.models.user_models import Users
from meal_max.utils.sql_utils import check_database_connection, check_table_exists


# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
# This bypasses standard security stuff we'll talk about later
# If you get errors that use words like cross origin or flight,
# uncomment this
# CORS(app)

# Initialize the BattleModel
Users = Users()

####################################################
#
# Healthchecks
#
####################################################


@app.route('/api/health', methods=['GET'])
def healthcheck() -> Response:
    """
    Health check route to verify the service is running.

    Returns:
        JSON response indicating the health status of the service.
    """
    app.logger.info('Health check')
    return make_response(jsonify({'status': 'healthy'}), 200)

@app.route('/api/db-check', methods=['GET'])
def db_check() -> Response:
    """
    Route to check if the database connection and meals table are functional.

    Returns:
        JSON response indicating the database health status.
    Raises:
        404 error if there is an issue with the database.
    """
    try:
        app.logger.info("Checking database connection...")
        check_database_connection()
        app.logger.info("Database connection is OK.")
        app.logger.info("Checking if locations table exists...")
        check_table_exists("locations")
        app.logger.info("locations table exists.")
        return make_response(jsonify({'database_status': 'healthy'}), 200)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 404)


##########################################################
#
# Locations
#
##########################################################


@app.route('/api/clear-locations', methods=['DELETE'])
def clear_catalog() -> Response:
    """
    Route to clear all locations (recreates the table).

    Returns:
        JSON response indicating success of the operation or error message.
    """
    try:
        app.logger.info("Clearing the locations")
        location_model.clear_locations()
        return make_response(jsonify({'status': 'success'}), 200)
    except Exception as e:
        app.logger.error(f"Error clearing locations: {e}")
        return make_response(jsonify({'error': str(e)}), 500)

@app.route('/api/delete-location/<int:location_id>', methods=['DELETE'])
def delete_meal(location_id: int) -> Response:
    """
    Route to delete a location by its ID. This performs a soft delete by marking it as deleted.

    Path Parameter:
        - location_id (int): The ID of the location to delete.

    Returns:
        JSON response indicating success of the operation or error message.
    """
    try:
        app.logger.info(f"Deleting meal by ID: {location_id}")

        location_model.delete_location(location_id)
        return make_response(jsonify({'status': 'success'}), 200)
    except Exception as e:
        app.logger.error(f"Error deleting location: {e}")
        return make_response(jsonify({'error': str(e)}), 500)

@app.route('/api/get-location-by-id/<int:location_id>', methods=['GET'])
def get_meal_by_id(location_id: int) -> Response:
    """
    Route to get a location by its ID.

    Path Parameter:
        - location_id (int): The ID of the location.

    Returns:
        JSON response with the location details or error message.
    """
    try:
        app.logger.info(f"Retrieving meal by ID: {location_id}")

        location = location_model.get_location_by_id(location_id)
        return make_response(jsonify({'status': 'success', 'location': location}), 200)
    except Exception as e:
        app.logger.error(f"Error retrieving meal by ID: {e}")
        return make_response(jsonify({'error': str(e)}), 500)

@app.route('/api/get-favorites-weather', methods=['GET'])
def get_meal_by_name(meal_name: str) -> Response:
    """
    Route to get a weather for all favorite locations

    Returns:
        JSON response with the weather details or error message.
    """
    try:
        app.logger.info(f"Retrieving weather of all favorite locatinos")

        weather = location_model.get_weather_for_favorite_locations()
        return make_response(jsonify({'status': 'success', 'weather': weather}), 200)
    except Exception as e:
        app.logger.error(f"Error retrieving weather for favorites: {e}")
        return make_response(jsonify({'error': str(e)}), 500)
    
@app.route('/api/get-favorites-forcast', methods=['GET'])
def get_meal_by_name(meal_name: str) -> Response:
    """
    Route to get a forecast for all favorite locations

    Returns:
        JSON response with the forecast details or error message.
    """
    try:
        app.logger.info(f"Retrieving forecast of all favorite locatinos")

        forecast = location_model.get_forecast_for_favorite_location()
        return make_response(jsonify({'status': 'success', 'forecast': forecast}), 200)
    except Exception as e:
        app.logger.error(f"Error retrieving forecast for favorites: {e}")
        return make_response(jsonify({'error': str(e)}), 500)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)