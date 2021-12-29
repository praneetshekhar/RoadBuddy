from flask.globals import request
import requests, os, re, json
import geocoder

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


def degDMStoDecimal(lat_lon):
    return float(lat_lon[1])+(float(lat_lon[2])/60)+(float(lat_lon[3])/3600)

def geocode(location_placename):
    # opencage geocoding api
    # using Denis Carriere's geocoder library
    # https://geocoder.readthedocs.io/providers/OpenCage.html#opencage

    api_key_opencage = os.getenv('OPENCAGE_API_KEY')
    g = geocoder.opencage(location_placename, key=api_key_opencage)
    geocoder_response = g.json['DMS']
    lat = geocoder_response['lat']
    lon = geocoder_response['lng']
    DMSregex = re.compile(r"([0-9]{1,2})°\s([0-9]{1,2})'\s([0-9]{1,2}\.?[0-9]+)''")
    lat = re.split(DMSregex, lat, maxsplit=3)
    lon = re.split(DMSregex, lon, maxsplit=3)
    return [degDMStoDecimal(lat),degDMStoDecimal(lon)]

print(mapbox_navigate('London', 'Southampton'))