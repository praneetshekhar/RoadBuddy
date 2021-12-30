#import json
#from itertools import islice
import requests, os

def pollutants(lat, lng):
    api_key_world_aqi = os.environ.get('WORLD_AQI_TOKEN')
    url = f"https://api.waqi.info/feed/geo:{lat};{lng}/"

    query = {"token": api_key_world_aqi}

    full_response = requests.request('GET', url, params=query)
    if full_response["status"] == "ok":
        
        pollutants = full_response['data']['iaqi']
        aqi = full_response['data']['aqi']
        
    return pollutants