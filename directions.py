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
### Hence, this is only needed if not running a server, like when debugging manually.        

def tomtom_getpoints(start, end):
    start_geocoded, end_geocoded = geocode(start), geocode(end)
    
    url = f"https://api.tomtom.com/routing/1/calculateRoute/{start_geocoded[0]},{start_geocoded[1]}:{end_geocoded[0]},{end_geocoded[1]}/json"
    #if optimization == 'least-polluted'
    maxRoutes = 2

    query_params = {"key": os.environ.get('TOMTOM_KEY'), "maxAlternatives": maxRoutes-1, "routeType": "eco"}
    response = requests.request('GET', url, params=query_params)
    response = response.json()

    #sample_dump = open('tests/sample.txt', 'w')
    #json.dump(response, sample_dump)
    #sample_dump.close()
    
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

    #start_time = time.perf_counter()

    popup_start = start + " " + str(route_coords_as_list[0])
    popup_end = end + " " +str(route_coords_as_list[len(route_coords_as_list)-1])

    map = folium.Map(location=route_coords_as_list[0], width='100%', height='100%')
    folium.Marker(location=route_coords_as_list[0], popup=popup_start, tooltip=start).add_to(map)
    folium.Marker(location=route_coords_as_list[len(route_coords_as_list)-1], popup=popup_end, tooltip=end).add_to(map)
    folium.vector_layers.PolyLine(route_coords_as_list).add_to(map)
    map.fit_bounds([list(route_coords_as_list[0]), list(route_coords_as_list[len(route_coords_as_list)-1])])

    #end_time = time.perf_counter()
    #duration = end_time - start_time
    #print("folium: ",duration)

    return map




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
    key = os.environ.get('MAPQUEST_KEY')
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
