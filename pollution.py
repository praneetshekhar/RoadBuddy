import requests, os
import statistics as stats
import pandas as pd

def pollutants(lat, lng):
    api_key_world_aqi = os.environ.get('WORLD_AQI_TOKEN')
    url = f"https://api.waqi.info/feed/geo:{lat};{lng}/"

    query = {"token": api_key_world_aqi}

    full_response = requests.request('GET', url, params=query).json()
    if full_response["status"] == "ok":
        
        pollutants = full_response['data']['iaqi'].values()
        pollutant_vector = [x['v'] for x in list(pollutants)]
        aqi = full_response['data']['aqi']
        pollution_loc_score = stats.median_high([stats.median_high(pollutant_vector), aqi])

    return pollution_loc_score

def routePollutionScore(route_df):
    radix = 0
    score = []
    while radix in range(len(route_df)):
        lat = route_df['latitude'][radix]
        lng = route_df['longitude'][radix]
        score.append(pollutants(lat,lng))
        radix += 1
    return stats.median_high(score)
