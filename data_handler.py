from re import A
import pandas as pd
import math
import json

def get_data(data):
    return pd.DataFrame(data)

def reduce_dataset(extended_dataframes, dist):
    df = extended_dataframes.copy(deep=True)
    optimized_df = pd.DataFrame(columns=['latitude','longitude'])
    df['latitude'] = [math.radians(x) for x in df['latitude']]
    df['longitude'] = [math.radians(x) for x in df['longitude']]

    dist = dist/1000
    dist_factor = 0.1 * dist
    
    radix = 0
    while radix < len(df):
        radix1 = radix+1
        while radix1 < len(df):
            latA = df['latitude'][radix]
            lngA = df['longitude'][radix]
            A = [latA, lngA]
            B = [df['latitude'][radix1], df['longitude'][radix1]]
            
            hvs = havesine(A,B)
            if hvs >= dist_factor:
                optimized_df.loc[len(optimized_df)] = B
                radix = radix1
                break
            radix1 += 1
        radix += 1
    
    optimized_df['latitude'] = [math.degrees(x) for x in optimized_df['latitude']]
    optimized_df['longitude'] = [math.degrees(x) for x in optimized_df['longitude']]
        
    return optimized_df


# Havesine formula for distance between a pair of lat/lng
def havesine(A, B):
    #A[0], A[1], B[0], B[1] = map(math.radians, [A[0], A[1], B[0], B[1]])
    dlng = abs(B[1] - A[1])
    dlat = abs(B[0] - A[0])

    a = math.sin(dlat/2.0)**2 + math.cos(A[0]) * math.cos(B[0]) * math.sin(dlng/2.0)**2
    c = 2 * math.asin(math.sqrt(a))
    km = 6378 * c
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