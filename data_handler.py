import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import haversine_distances
import time, json

def get_data(data):
    return pd.DataFrame(data)

def reduce_dataset(routes_list, route_number):
    #df = get_data(routes_list[route_number]['coords'])
    df = routes_list[route_number]['coords']
    optimized_df = pd.DataFrame(columns=['latitude','longitude'])
    
    dist = routes_list[route_number]['route_distance']/1000
    dist_factor = 0.1 * dist
    
    ## Redundant code below
    '''
    start_time = time.perf_counter()
    radix1 = -1
    while radix1 < len(df):
        radix1 += 1
        radix2 = radix1+1
        while radix2 < len(df):
            lat1, lng1 = df[radix1]['latitude'], df[radix1]['longitude']
            lat2, lng2 = df[radix2]['latitude'], df[radix2]['longitude']
            
            hvs = haversine(lat1,lng1,lat2,lng2)
            if hvs >= dist_factor:
                optimized_df = optimized_df.append({'latitude': lat2, 'longitude': lng2}, ignore_index=True)
                radix1 = radix2
                break
            radix2 += 1
    end_time = time.perf_counter()
    duration = end_time - start_time
    print("reduce_dataset - np: ", duration)
    '''

    #start_time = time.perf_counter()

    #vect_df = pd.DataFrame(col)

    optimized_df = pd.DataFrame(columns=['latitude','longitude'])
    radix1 = -1
    while radix1 < len(df):
        radix1 += 1
        radix2 = radix1+1
        while radix2 < len(df):
            ptA = [df[radix1]['latitude'], df[radix1]['longitude']]
            ptB = [df[radix2]['latitude'], df[radix2]['longitude']]
            ptA_rad = [np.radians(_) for _ in ptA]
            ptB_rad = [np.radians(_) for _ in ptB]
            hvs = haversine_distances([ptA_rad], [ptB_rad]) 
            hvs = hvs * 6378
            if hvs[0][0] >= dist_factor:
                optimized_df = optimized_df.append({'latitude': ptB[0], 'longitude': ptB[1]}, ignore_index=True)
                radix1 = radix2
                break
            radix2 += 1

    #end_time = time.perf_counter()
    #duration = end_time - start_time
    #print("reduce_dataset - sklearn: ",duration)
    #optimized_df['latitude'] = [np.degrees(x) for x in optimized_df['latitude']]
    #optimized_df['longitude'] = [np.degrees(x) for x in optimized_df['longitude']]
    #print(len(optimized_df))
    return optimized_df #usable route for pollution score calculation


# Haversine formula for distance between a pair of lat/lng
# Usage replaced by sklearn in version-33 - 2x time improvement
def haversine(latA, lngA, latB, lngB):
    
    latA, lngA, latB, lngB = map(np.radians, [latA, lngA, latB, lngB])
    dlng = abs(lngB - lngA)
    dlat = abs(latB - latA)

    a = np.sin(dlat/2.0)**2 + np.cos(latA) * np.cos(latB) * np.sin(dlng/2.0)**2
    c = 2 * np.arcsin(np.sqrt(a))
    km = 6378 * c
    
    latA, lngA, latB, lngB = map(np.degrees, [latA, lngA, latB, lngB])

    return km

"""
#Test Cases
#bom = [19.0759899, 72.8773928]
#pnc = [18.521428, 73.8544541]
#print(havesine(bom,pnc))

with open("tests/sample.txt","r") as file:
    response = json.load(file)


#optimized = reduce_dataset(df_test, 0)
#print(len(optimized))
#print(optimized)
#import pollution
#print(type(pollution.routePollutionScore(optimized)))
"""