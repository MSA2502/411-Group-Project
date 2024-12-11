#!/bin/bash

# Define the base URL for the Flask API
BASE_URL="http://localhost:5000/api"

# Flag to control whether to echo JSON output
ECHO_JSON=false

# Parse command-line arguments
while [ "$#" -gt 0 ]; do
  case $1 in
    --echo-json) ECHO_JSON=true ;;
    *) echo "Unknown parameter passed: $1"; exit 1 ;;
  esac
  shift
done


###############################################
#
# Health checks
#
###############################################

# Function to check the health of the service
check_health() {
  echo "Checking health status..."
  curl -s -X GET "$BASE_URL/health" | grep -q '"status": "healthy"'
  if [ $? -eq 0 ]; then
    echo "Service is healthy."
  else
    echo "Health check failed."
    exit 1
  fi
}

# Function to check the database connection
check_db() {
  echo "Checking database connection..."
  curl -s -X GET "$BASE_URL/db-check" | grep -q '"database_status": "healthy"'
  if [ $? -eq 0 ]; then
    echo "Database connection is healthy."
  else
    echo "Database check failed."
    exit 1
  fi
}


##########################################################
#
# Location Management
#
##########################################################

clear_locations() {
  echo "Clearing the locations..."
  curl -s -X DELETE "$BASE_URL/clear-locations" | grep -q '"status": "success"'
}


create_location() {
  location=$1

  echo "Adding location: ($location)"
  curl -s -X POST "$BASE_URL/create-location" -H "Content-Type: application/json" \
    -d "{\"location\":\"$location\"}" | grep -q '"status": "success"'
  if [ $? -eq 0 ]; then
    echo "Location added successfully."
  else
    echo "Failed to add location."
    exit 1
  fi
}

delete_location() {
  location_id=$1

  echo "Deleting location by ID ($location_id)..."
  response=$(curl -s -X DELETE "$BASE_URL/delete-location/$location_id")
  #echo $?
  if echo "$response" | grep -q '"status": "success"'; then
    echo "location deleted successfully by ID ($location_id)."
  else
    echo "Failed to delete location by ID ($location_id)."
    exit 1
  fi
}

get_location_by_id() {
  location_id=$1

  echo "Getting location by ID ($location_id)..."
  response=$(curl -s -X GET "$BASE_URL/get-location-by-id/$location_id")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Location retrieved successfully by ID ($location_id)."
    if [ "$ECHO_JSON" = true ]; then
      echo "Location JSON (ID $location_id):"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get location by ID ($location_id)."
    exit 1
  fi
}

get_weather_for_location() {
  location_id=$1

  echo "Getting weather for location $location_name"
  response=$(curl -s -X GET "$BASE_URL/get-weather-for_location/$location_name")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Weather retrieved successfully by name."
    if [ "$ECHO_JSON" = true ]; then
      echo "Weather JSON (by id):"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get weather by location id."
    exit 1
  fi
}


############################################################
#
# Sign In
#
############################################################

login() {
  username=$1
  password=$2

  echo "Logging in: ($username)"
  curl -s -X POST "$BASE_URL/login" -H "Content-Type: application/json" \
    -d "{\"username\":\"$username\", \"password\":\"$password\"}" | grep -q '"status": "success"'
  if [ $? -eq 0 ]; then
    echo "Login succesful."
  else
    echo "Login Failed."
    exit 1
  fi
}

create_account() {
  username=$1
  password=$2

  echo "Logging in: ($username)"
  curl -s -X POST "$BASE_URL/create-account" -H "Content-Type: application/json" \
    -d "{\"username\":\"$username\", \"password\":\"$password\"}" | grep -q '"status": "success"'
  if [ $? -eq 0 ]; then
    echo "Account create succesful."
  else
    echo "Account create Failed."
    exit 1
  fi
}

update_password() {
  username=$1
  password=$2

  echo "Logging in: ($username)"
  curl -s -X POST "$BASE_URL/update-password" -H "Content-Type: application/json" \
    -d "{\"username\":\"$username\", \"password\":\"$password\"}" | grep -q '"status": "success"'
  if [ $? -eq 0 ]; then
    echo "Password Update succesful."
  else
    echo "Password Update Failed."
    exit 1
  fi
}

# Health checks
check_health
check_db

# Clear the locations
clear_locations

# Create locations
create_location "Boston"  
create_location "Paris"  
create_location "Rome" 
create_location "San Francisco"  
create_location "Atlanta" 

get_location_by_id "1"
get_weather_for_location "1"
delete_location "1"


create_account "test" "test"
login "test" "test"
update_password "test" "new_pass"



echo "All tests passed successfully!"