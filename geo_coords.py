#!/bin/python3

import logging

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

import pandas as pd
import numpy as np
from tqdm import tqdm

from time import sleep

def get_geo_coords(address, attempt=1, max_attempts=5):

    try:
        locator = Nominatim(user_agent = 'myGeocoder')
        location = locator.geocode(address, timeout=5)
        
        if location == None:
            #print(location)
            return np.nan, np.nan
        else: 
            return location.latitude, location.longitude
    except GeocoderTimedOut:
        if attempt <= max_attempts:
            return get_geo_coords(address, attempt = attempt+1)
        raise

def main():

    filename = "/Users/emanuel.holgersson/Documents/Python/REST_APIs/football_statistics_teams_1.csv"
    df = pd.read_csv(filename, encoding='utf-8')
    lat = []
    lon = []
    for address in tqdm(df['venue.name']):

        if address == None:
            lat.append(np.nan)
            lon.append(np.nan)
        else:
            lat_tmp,lon_tmp = get_geo_coords(address)

            lat.append(lat_tmp)
            lon.append(lon_tmp)
        
        sleep(1)
        

    df['lat'] = lat
    df['lon'] = lon

    df.to_csv("/Users/emanuel.holgersson/Documents/Python/REST_APIs/football_statistics_teams_2.csv", encoding='utf-8', index=False)


if __name__ == '__main__':
    main()

    #lat_tmp,lon_tmp  = get_geo_coords("Mill Farm Stadium")

    #print(lat_tmp,lon_tmp)
    
