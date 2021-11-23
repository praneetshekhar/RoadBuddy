import requests, os, re
import geocoder

def mapbox_navigate(start, end):
    # mapbox api
    api_token_mapbox = os.environ.get('MAPBOX_ACCESS_TOKEN')
    url = "https://api.mapbox.com/directions/v5/mapbox/driving/"


def degDMStoDecimal(latlon):
    return float(latlon[1])+(float(latlon[2])/60)+(float(latlon[3])/3600)

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