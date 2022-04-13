from flask.globals import request
import requests, os, re, json, time
import geocoder
import data_handler as dh
import pandas as pd
from pollution import routePollutionScore
import folium

#from dotenv import load_dotenv
#load_dotenv()
### Flask loads the nearest .env or .flaskenv automatically and does the load_dotenv()
### Hence, this is only needed if not running a flask instance, like when running via gunicorn.

def tomtom_getpoints(start, end):
    start_geocoded, end_geocoded = geocode(start), geocode(end)
    
    url = f"https://api.tomtom.com/routing/1/calculateRoute/{start_geocoded[0]},{start_geocoded[1]}:{end_geocoded[0]},{end_geocoded[1]}/json"
    #if optimization == 'least-polluted'
    maxRoutes = 2

    query_params = {"key": os.environ.get('TOMTOM_KEY'), "maxAlternatives": maxRoutes-1, "routeType": "eco"}
    response = requests.request('GET', url, params=query_params)
    response = response.json()
    
    routes = []
    if 'routes' in response:
        n_routes = len(response['routes'])
        if n_routes > 0:

            for i in range(n_routes):
                routes.append(get_points(response, i))
                usable_route = dh.reduce_dataset(routes, i) # reduce dataset for pollution score
                routes[i].update({'routePollutionScore': routePollutionScore(usable_route)})
    
    return routes

# get points from API data
def get_points(tomtom_api_response, route_number):
    return {'coords': tomtom_api_response["routes"][route_number]["legs"][0]["points"],
    'route_distance': tomtom_api_response["routes"][route_number]["summary"]["lengthInMeters"]}


#clean data for polyline utility
def clean_coords(route_as_pandas_df):
    route_coords_list = [x for x in zip(route_as_pandas_df['latitude'],route_as_pandas_df['longitude'])]
    return route_coords_list

# mapping utility
def get_folium_map(route_coords_as_list, start, end):

    popup_start = start + " " + str(route_coords_as_list[0])
    popup_end = end + " " +str(route_coords_as_list[len(route_coords_as_list)-1])

    map = folium.Map(location=route_coords_as_list[0], width='100%', height='100%')
    folium.Marker(location=route_coords_as_list[0], popup=popup_start, tooltip=start).add_to(map)
    folium.Marker(location=route_coords_as_list[len(route_coords_as_list)-1], popup=popup_end, tooltip=end).add_to(map)
    folium.vector_layers.PolyLine(route_coords_as_list).add_to(map)
    map.fit_bounds([list(route_coords_as_list[0]), list(route_coords_as_list[len(route_coords_as_list)-1])])

    return map


def geocode(location_placename):
    # opencage geocoding api
    # using Denis Carriere's geocoder library
    # https://geocoder.readthedocs.io/providers/OpenCage.html#opencage

    api_key_opencage = os.environ.get('OPENCAGE_API_KEY')
    g = geocoder.opencage(location_placename, key=api_key_opencage)
    
    if g.json['status'] == 'OK':
        lat = g.json['lat']
        lng = g.json['lng']
    
    return tuple([lat, lng])