Route: /create-user
    ● Request Type: POST
    ● Purpose: Creates a new user account with a username and password.
    ● Request Body:
        ○ username (String): User's chosen username.
        ○ password (String): User's chosen password.
    ● Response Format: JSON
    ○ Success Response Example:
        ■ Code: 200
        ■ Content: { "message": "Account created successfully" }
    ● Example Request:
        {
        "username": "newuser123",
        "password": "securepassword"
        }
    ● Example Response:
        {
        "message": "Account created successfully",
        "status": "200"
        }

Route: /update-password
    ● Request Type: POST
    ● Purpose: Updates the password of a users account
    ● Request Body:
        ○ username (String): User's chosen username.
        ○ password (String): User's chosen password.
    ● Response Format: JSON
    ○ Success Response Example:
        ■ Code: 200
        ■ Content: { "message": "Password updated successfully" }
    ● Example Request:
        {
        "username": "newuser123",
        "password": "securepassword"
        }
    ● Example Response:
        {
        "message": "Password updated successfully",
        "status": "200"
        }

Route: /api/get-favorites-forcast
    ● Request Type: GET
    ● Purpose: Get the forcast for a favorited location
    ● Request Body:
        ○ username (String): User's chosen username.
        ○ password (String): User's chosen password.
    ● Response Format: JSON
    ○ Success Response Example:
        ■ Code: 200
        ■ Content: { "message": "Password updated successfully" }
    ● Example Request:
        {
        "username": "newuser123",
        "password": "securepassword"
        }
    ● Example Response:
        {
        "message": "Password updated successfully",
        "status": "200"
        }