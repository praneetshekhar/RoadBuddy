#import json
import requests, os
from itertools import islice

def pollutants()
    api_key_ambee = os.environ.get('AMBEE_API_KEY')
    url = "https://api.ambeedata.com/latest/by-lat-lng"

    query = {"lat": lat, "lng": lon }

    headers = {
        'x-api-key' : api_key,
        'Content-type' : 'application/json' 
    }

    full_response = requests.request('GET', url, headers=headers, params=query)
    if full_response["message"] == "success":
        pollutants = list(islice(full_response["stations"][0].items(),6))
        aqi = full_response["stations"][0]["AQI"]
        aqi_details = full_response["stations"][0]["aqiInfo"]