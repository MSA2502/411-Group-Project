Route: /api/create-account
    ● Request Type: POST
    ● Purpose: Creates a new user account with a username and password.
    ● Request Body:
        ○ username (String): User's chosen username.
        ○ password (String): User's chosen password.
    ● Response Format: JSON
    ○ Success Response Example:
        ■ Code: 201
        ■ Content: { "message": "Account created successfully" }
    ● Example Request:
        {
        "username": "newuser123",
        "password": "securepassword"
        }
    ● Example Response:
        {
        "message": "Account created successfully",
        "status": "201"
        }

Route: /api/update-password
    ● Request Type: POST
    ● Purpose: Updates the password of a users account
    ● Request Body:
        ○ username (String): User's chosen username.
        ○ password (String): User's chosen password.
    ● Response Format: JSON
    ○ Success Response Example:
        ■ Code: 201
        ■ Content: { "message": "Password updated successfully" }
    ● Example Request:
        {
        "username": "newuser123",
        "password": "securepassword"
        }
    ● Example Response:
        {
        "message": "Password updated successfully",
        "status": "201"
        }

Route: /api/login
    ● Request Type: POST
    ● Purpose: Login a user
    ● Request Body:
        ○ username (String): User's chosen username.
        ○ password (String): User's chosen password.
    ● Response Format: JSON
    ○ Success Response Example:
        ■ Code: 201
        ■ Content: { "message": "Login sucessful" }
    ● Example Request:
        {
        "username": "newuser123",
        "password": "securepassword"
        }
    ● Example Response:
        { "message": "Login sucessful" }

Route: /api/health
    ● Request Type: GET
    ● Purpose: Route to check if the database connection and location and users table are functional.
    ● Response Format: JSON
    ○ Success Response Example:
        ■ Code: 200
        ■ Content: { "database_status": "healthy" }
    ● Example Response:
        { "database_status": "healthy" }

Route: /api/create_location
    ● Request Type: POST
    ● Purpose: Creates a location
    ● Request Body:
        ○ location (String): the location name.
    ● Response Format: JSON
    ○ Success Response Example:
        ■ Code: 201
        ■ Content: { "status": "success", "location": location }
    ● Example Request:
        {
        "location": "boston"
        }
    ● Example Response:
        {
        "status": "success",
        "location": 
            {
            "id": 0,
            "location": "boston",
            "current_weather": "(Mist (mist), Temp: 1.09\u00b0C, Humidity: 92%)"
            } 
        }

Route: /api/clear_locations
    ● Request Type: DELETE
    ● Purpose: Clears all locations
    ● Response Format: JSON
    ○ Success Response Example:
        ■ Code: 200
        ■ Content: { "status": "success" }
    ● Example Response:
        { "status": "success" }

Route: /api/delete-location/<int:location_id>
    ● Request Type: DELETE
    ● Purpose: Deletes a specific location
    ● Response Format: JSON
    ● Path Parameter: 
        ○ location_id (int): the id of the location to delete.
    ○ Success Response Example:
        ■ Code: 200
        ■ Content: { "status": "success" }
    ● Example Response:
        { "status": "success" }

Route: /api/get-location-by-id/<int:location_id>
    ● Request Type: GET
    ● Purpose: Route to get a location by its ID.
    ● Response Format: JSON
    ● Path Parameter: 
        ○ location_id (int): the id of the location to get.
    ○ Success Response Example:
        ■ Code: 201
        ■ Content: { "status": "success", "location": location }
    ● Example Response:
        {
        "status": "success",
        "location": "Boston"
        }

Route: /api/get-weather-for_location/<int:location>
    ● Request Type: GET
    ● Purpose: Route to get a the weather for a location
    ● Response Format: JSON
    ● Path Parameter: 
        ○ location_id (int): the id of the location to get.
    ○ Success Response Example:
        ■ Code: 201
        ■ Content: { "status": "success", "location": location }
    ● Example Response:
        {
        "status": "success",
        "weather": "(Mist (mist), Temp: 1.09\u00b0C, Humidity: 92%)"
        }