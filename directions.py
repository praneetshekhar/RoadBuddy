from flask.globals import request
import requests, os, re, json
import geocoder
import data_handler as dh
import pandas as pd
from pollution import routePollutionScore
import polyline

#from dotenv import load_dotenv
#load_dotenv()
### Flask loads the nearest .env or .flaskenv automatically and does the load_dotenv()
### Hence, this is only needed if not running a server, like when debugging manually.

def tomtom_getpoints(start, end):
    start, end = geocode(start), geocode(end)
    url = f"https://api.tomtom.com/routing/1/calculateRoute/{start[0]},{start[1]}:{end[0]},{end[1]}/json"
    query_params = {"key": os.environ.get('TOMTOM_KEY'), "maxAlternatives": 1, "routeType": "eco"}
    response = requests.request('GET', url, params=query_params)
    response = response.json()

    n_routes = len(response["routes"])
    if n_routes == 2:
        coords = response["routes"][0]["legs"][0]["points"]
        route_dist = response["routes"][0]["summary"]["lengthInMeters"]
        coords1 = response["routes"][1]["legs"][0]["points"]
        route1_dist = response["routes"][1]["summary"]["lengthInMeters"]
        route = dh.get_data(coords)
        route1 = dh.get_data(coords1)

        usable_route = dh.reduce_dataset(route, route_dist)
        usable_route1 = dh.reduce_dataset(route1, route1_dist)
        route1_score = routePollutionScore(usable_route)
        route2_score = routePollutionScore(usable_route1)
        if route1_score < route2_score:
            route = 1
            least_polluted_route = usable_route
            cleaned_coords = clean_coords(route)
        else:
            route = 2
            least_polluted_route = usable_route1
            cleaned_coords = clean_coords(route1)
        
        polyline_route = polyline.encode(cleaned_coords)
    
    return {"optimizedRoute": least_polluted_route, "polyline": polyline_route}


#clean data for polyline utility
def clean_coords(pandas_route):
    route_coords = [x for x in zip(pandas_route['latitude'],pandas_route['longitude'])]
    return route_coords

#Deprecated, waypoints functionality might still be useful
def mapbox_navigate(start, end):
    # mapbox api
    api_token_mapbox = os.environ.get('MAPBOX_ACCESS_TOKEN')
    start_gid, end_gid = geocode(start), geocode(end)
    url = f"https://api.mapbox.com/directions/v5/mapbox/driving/{start_gid[0]},{start_gid[1]};{end_gid[0]},{end_gid[1]}?geometries=geojson&access_token={api_token_mapbox}"
    map_route_response = requests.request('GET', url).json()
    location_gradients = []
    if map_route_response['code'] == 'Ok':
        locations_coords = map_route_response['routes'][0]['geometry']['coordinates']
        waypoints = map_route_response['waypoints']
        for i in range(len(waypoints)):
            location_gradients.append(waypoints[i]['location'])
        return location_gradients
    else:
        return location_gradients  

#Deprecated
def mapquest_api(start, destination):
    key = "TAfEZarizs3jiXkQ9ZgxvLOVEqIPFuHH"
    url = f"http://www.mapquestapi.com/directions/v2/alternateroutes?key={key}&outFormat=xml"
    headers = {"content-type": "application/json"}
    payload = json.dumps({
            "locations": [
            start,
            destination
        ],
        "maxRoutes": 2
    })
    response_mapquest = requests.request("POST", url, headers=headers, data=payload)
    if response_mapquest.status_code == 200:
        data = response_mapquest.json()
    else:
        data = {"response": response_mapquest.status_code}
    return data

#conversion utility
def degDMStoDecimal(lat_lon):
    unsigned_lat_lon = float(lat_lon[1])+(float(lat_lon[2])/60)+(float(lat_lon[3])/3600)
    if lat_lon[4] in ['W', 'S']:
        return unsigned_lat_lon * -1
    else:
        return unsigned_lat_lon

def geocode(location_placename):
    # opencage geocoding api
    # using Denis Carriere's geocoder library
    # https://geocoder.readthedocs.io/providers/OpenCage.html#opencage

    api_key_opencage = os.environ.get('OPENCAGE_API_KEY')
    g = geocoder.opencage(location_placename, key=api_key_opencage)
    # if g is not None
    geocoder_response = g.json['DMS']
    lat = geocoder_response['lat']
    lon = geocoder_response['lng']
    DMSregex = re.compile(r"([0-9]{1,2})°\s([0-9]{1,2})'\s([0-9]{1,2}\.?[0-9]+)''\s(W|E|N|S)")
    lat = re.split(DMSregex, lat)
    lon = re.split(DMSregex, lon)
    return tuple([degDMStoDecimal(lat),degDMStoDecimal(lon)])
