import requests
import json
import sys 
import os
from set_api_key import read_api_key


    
def get_lat_long(place_name, ):
    url = "https://maps.googleapis.com/maps/api/geocode/json"

    # Parameters for the API request
    api_key = read_api_key(3141)
    params = {
        "address": place_name,
        "key": api_key
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()

        if data['status'] == 'OK':
            # Extract latitude and longitude
            latitude = data['results'][0]['geometry']['location']['lat']
            longitude = data['results'][0]['geometry']['location']['lng']
            return latitude, longitude
        else:
            return "No results found", None
    else:
        return "Request failed with status code " + str(response.status_code), None


if __name__ == "__main__":
    
    #set_api_key()
    
    # Replace 'Place Name' with your desired place
    place_name = 'Santa Clara University'
    api_key = os.environ.get('GOOGLE_API_KEY')
    lat, long = get_lat_long(place_name, api_key)
    print("Latitude:", lat, "Longitude:", long)
