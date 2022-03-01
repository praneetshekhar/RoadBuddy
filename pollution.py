import requests, os
import statistics as stats
import pandas as pd
import math, time

def pollutants(lat, lng):
    #start_time = time.perf_counter()
    #api_key_world_aqi = os.environ.get('WORLD_AQI_TOKEN')
    #url = f"https://api.waqi.info/feed/geo:{lat};{lng}/"

    #query = {"token": api_key_world_aqi}

    key = os.environ.get('OPENWEATHER_API_KEY')
    query = {"lat": lat, "lon": lng, "appid": key}
    url_for_current_data = 'http://api.openweathermap.org/data/2.5/air_pollution

    full_response = requests.request('GET', url_for_current_data, params=query)
    if full_response.status_code == 200:

        full_response = full_response.json()
        #pollutants = full_response['data']['iaqi'].values()
        pollutants = full_response['list'][0]['components'].values()
        #pollutant_vector = [x['v'] for x in list(pollutants)]
        pollutant_vector = list(pollutants)
        aqi = full_response['list'][0]['main']['aqi']
        pollution_loc_score = stats.median_high([stats.median_high(pollutant_vector), aqi])
        
        return pollution_loc_score
    #end_time = time.perf_counter()
    #duration = end_time - start_time
    #print("pollutants: ",duration)

    return -1

##  Major overhaul upcoming
# applying machine learning algorithms of various kinds and magnitudes to get the best out of the data is the next step
def routePollutionScore(route_df):
    start_time = time.perf_counter()
    radix = 0
    score = []
    
    lat_lng = route_df.values

    for radix in range(len(route_df)):
        lat = lat_lng[radix][0]
        lng = lat_lng[radix][1]
        
        score.append(pollutants(lat,lng))
    
    end_time = time.perf_counter()
    duration = end_time - start_time
    print("routepollutionscore: ",duration)

    return stats.median_high(score)
