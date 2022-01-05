from re import A
import pandas as pd
import numpy as np


def get_data(data):
    return pd.DataFrame(data)

def reduce_dataset(routes_list, route_number):
    
    df = get_data(routes_list[route_number]['coords'])

    optimized_df = pd.DataFrame(columns=['latitude','longitude'])
    
    dist = routes_list[route_number]['route_distance']/1000
    dist_factor = 0.1 * dist
    
    radix = 0
    while radix < len(df):
        radix1 = radix+1
        while radix1 < len(df):
            A = [df['latitude'][radix], df['longitude'][radix]]
            B = [df['latitude'][radix1], df['longitude'][radix1]]
            
            hvs = havesine(A,B)
            if hvs >= dist_factor:
                optimized_df.loc[len(optimized_df)] = B
                radix = radix1
                break
            radix1 += 1
        radix += 1
    
    #optimized_df['latitude'] = [np.degrees(x) for x in optimized_df['latitude']]
    #optimized_df['longitude'] = [np.degrees(x) for x in optimized_df['longitude']]
            
    return optimized_df #usable route for pollution score calculation


# Havesine formula for distance between a pair of lat/lng
def havesine(A, B):
    A[0], A[1], B[0], B[1] = map(np.radians, [A[0], A[1], B[0], B[1]])
    dlng = abs(B[1] - A[1])
    dlat = abs(B[0] - A[0])

    a = np.sin(dlat/2.0)**2 + np.cos(A[0]) * np.cos(B[0]) * np.sin(dlng/2.0)**2
    c = 2 * np.arcsin(np.sqrt(a))
    km = 6378 * c
    
    A[0], A[1], B[0], B[1] = map(np.degrees, [A[0], A[1], B[0], B[1]])

    return km

"""
#Test Cases
#bom = [19.0759899, 72.8773928]
#pnc = [18.521428, 73.8544541]
#print(havesine(bom,pnc))

with open("tests/sample.txt","r") as file:
    response = json.load(file)

df_test = get_data(response["routes"][1]["legs"][0]["points"])
dist_route = response["routes"][1]["summary"]["lengthInMeters"]
print(len(df_test))
optimized = reduce_dataset(df_test,dist_route)
print(len(optimized))
print(optimized)
import pollution
#print(type(pollution.routePollutionScore(optimized)))
"""