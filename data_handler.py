import pandas as pd
from pandas.core.frame import DataFrame
import math

def get_data(data):
    return pd.DataFrame(data)

def reduce_dataset(extended_dataframes, dist):
    df = extended_dataframes
    optimized_df = pd.DataFrame(df.loc[[0]], columns=['latitude','longitude'])

    dist = dist/1000
    if dist <= 10 or dist<=30:
        dist_factor = 0.3 * dist
    else:
        dist_factor = 30
    
    radix = 0
    while radix in range(len(df)):
        latA = df['latitude'][radix]
        lngA = df['longitude'][radix]
        A = [latA, lngA]
        radix1 = radix+1
        while radix1 < len(df):
            B = [df['latitude'][radix1], df['longitude'][radix1]]
            
            hvs = havesine(A,B)
            if hvs >= dist_factor:
                optimized_df.loc[len(optimized_df)] = B
                radix = radix1
                break
            else:
                radix1 += 1
        radix += 1
    
    return optimized_df


# Havesine formula for distance between a pair of lat/lng
def havesine(A, B):
    A[0], A[1], B[0], B[1] = map(math.radians, [A[0], A[1], B[0], B[1]])
    dlng = abs(B[1] - A[1])
    dlat = abs(B[0] - A[0])

    a = math.sin(dlat/2.0)**2 + math.cos(A[0]) * math.cos(B[0]) * math.sin(dlng/2.0)**2
    c = 2 * math.asin(math.sqrt(a))
    km = 6378 * c
    return km
