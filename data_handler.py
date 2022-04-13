import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import haversine_distances

def get_data(data):
    return pd.DataFrame(data)

def reduce_dataset(routes_list, route_number):

    df = routes_list[route_number]['coords']
    optimized_df = pd.DataFrame(columns=['latitude','longitude'])
    
    dist = routes_list[route_number]['route_distance']/1000
    dist_factor = 0.1 * dist    

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

    return optimized_df #usable route for pollution score calculation