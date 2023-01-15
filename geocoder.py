import pandas as pd
import geopy
from geopy.geocoders import ArcGIS

def geocoder(filename):
    nom = ArcGIS()
    df = pd.read_csv(filename)
    print(df.columns)
    if ('address' not in df.columns) and ('Address' not in df.columns):
        return False 
    else:
        df["Coordinates"] = df["Address"].apply(nom.geocode)        
        df["Latitude"] = df["Coordinates"].apply(lambda x: x.latitude if x != None else None)
        df["Longitude"] = df["Coordinates"].apply(lambda x: x.latitude if x != None else None)
        df = df.drop(columns="Coordinates", index=None)
        return df


#print(geocoder('test.csv'))
