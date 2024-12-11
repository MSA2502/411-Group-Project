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

# Initialize the UsersModel
users = Users()

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
    Route to check if the database connection and location table are functional.

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
@app.route('/api/create_location', methods=['POST'])
def create_location() -> Response:
    """
    Route to create a location

    Expected JSON Input:
        - location (str): The location.

    Returns:
        JSON response indicating the success of creating a location.
    Raises:
        400 error if input validation fails.
        500 error if there is an issue updating the password.
    """
    app.logger.info('Creating new user')
    try:
        # Get the JSON data from the request
        data = request.get_json()

        # Extract and validate required fields
        location = data.get('location')

        if not location:
            return make_response(jsonify({'error': 'Invalid input, all fields are required with valid values'}), 400)

        app.logger.info('Creating location: %s', location)
        location = location_model.create_location(location)

        app.logger.info("Created location: %s", location)
        return make_response(jsonify({'status': 'success', 'location': location}), 201)
    except Exception as e:
        app.logger.error("Failed to create", str(e))
        return make_response(jsonify({'error': str(e)}), 500)

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
def delete_location(location_id: int) -> Response:
    """
    Route to delete a location by its ID. This performs a soft delete by marking it as deleted.

    Path Parameter:
        - location_id (int): The ID of the location to delete.

    Returns:
        JSON response indicating success of the operation or error message.
    """
    try:
        app.logger.info(f"Deleting location by ID: {location_id}")

        location_model.delete_location(location_id)
        return make_response(jsonify({'status': 'success'}), 200)
    except Exception as e:
        app.logger.error(f"Error deleting location: {e}")
        return make_response(jsonify({'error': str(e)}), 500)

@app.route('/api/get-location-by-id/<int:location_id>', methods=['GET'])
def get_location_by_id(location_id: int) -> Response:
    """
    Route to get a location by its ID.

    Path Parameter:
        - location_id (int): The ID of the location.

    Returns:
        JSON response with the location details or error message.
    """
    try:
        app.logger.info(f"Retrieving location by ID: {location_id}")

        location = location_model.get_location_by_id(location_id)
        return make_response(jsonify({'status': 'success', 'location': location}), 200)
    except Exception as e:
        app.logger.error(f"Error retrieving location by ID: {e}")
        return make_response(jsonify({'error': str(e)}), 500)

@app.route('/api/get-weather-for_location/<int:location>', methods=['GET'])
def get_weather_for_location(location_id: int) -> Response:
    """
    Route to get a weather for a specific location

    Path Parameter:
        - location_id (id): The ID of the location to get the weather for.

    Returns:
        JSON response with the weather details or error message.
    """
    try:
        app.logger.info(f"Retrieving weather of all favorite locations")

        weather = location_model.get_weather_for_location(location_id)
        return make_response(jsonify({'status': 'success', 'weather': weather}), 200)
    except Exception as e:
        app.logger.error(f"Error retrieving weather for location: {e}")
        return make_response(jsonify({'error': str(e)}), 500)
    
##########################################################
#
# Users
#
##########################################################

@app.route('/api/login', methods=['POST'])
def login() -> Response:
    """
    Route to login

    Expected JSON Input:
        - username (str): The username.
        - password (str): The password.

    Returns:
        JSON response indicating the success of the user login.
    Raises:
        400 error if input validation fails.
        401 error if invalid password.
        500 error if there is an issue loging in.
    """
    app.logger.info('Creating new user')
    try:
        # Get the JSON data from the request
        data = request.get_json()

        # Extract and validate required fields
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return make_response(jsonify({'error': 'Invalid input, all fields are required with valid values'}), 400)

        app.logger.info('Attempting loging for: %s', username)
        if users.check_password(username, password):
            app.logger.info("Updated password for user: %s", username)
            return make_response(jsonify({'status': 'success', 'message': 'Password updated successfully'}), 201)
        else:
            app.logger.info("Failed to login user: %s", username)
            return make_response(jsonify({'status': 'error', 'message': 'Incorrect Password'}), 401)

    except Exception as e:
        app.logger.error("Failed to login user: %s", str(e))
        return make_response(jsonify({'error': str(e)}), 500)

@app.route('/api/create-account', methods=['POST'])
def create_account() -> Response:
    """
    Route to add a new user

    Expected JSON Input:
        - username (str): The username.
        - password (str): The password.

    Returns:
        JSON response indicating the success of the user addition.
    Raises:
        400 error if input validation fails.
        500 error if there is an issue adding the user to the database.
    """
    app.logger.info('Creating new user')
    try:
        # Get the JSON data from the request
        data = request.get_json()

        # Extract and validate required fields
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return make_response(jsonify({'error': 'Invalid input, all fields are required with valid values'}), 400)

        # Check that price is a float and has at most two decimal places

        # Call the kitchen_model function to add the combatant to the database
        app.logger.info('Adding user: %s', username)
        users.create_user(username, password)

        app.logger.info("User added: %s", username)
        return make_response(jsonify({'status': 'success', 'message': 'Account created successfully'}), 201)
    except Exception as e:
        app.logger.error("Failed to add user: %s", str(e))
        return make_response(jsonify({'error': str(e)}), 500)
    
@app.route('/api/update-password', methods=['POST'])
def update_password() -> Response:
    """
    Route to update the password for a user

    Expected JSON Input:
        - username (str): The username.
        - password (str): The password.

    Returns:
        JSON response indicating the success of the user addition.
    Raises:
        400 error if input validation fails.
        500 error if there is an issue updating the password.
    """
    app.logger.info('Creating new user')
    try:
        # Get the JSON data from the request
        data = request.get_json()

        # Extract and validate required fields
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return make_response(jsonify({'error': 'Invalid input, all fields are required with valid values'}), 400)

        app.logger.info('Update password for user: %s', username)
        users.update_password(username, password)

        app.logger.info("Updated password for user: %s", username)
        return make_response(jsonify({'status': 'success', 'message': 'Password updated successfully'}), 201)
    except Exception as e:
        app.logger.error("Failed to update password for user: %s", str(e))
        return make_response(jsonify({'error': str(e)}), 500)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)