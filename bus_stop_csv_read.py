"""
@fileName: bus_stop_csv_read.py
@Author:
Sai Manogna Pentyala - spentyal@andrew.cmu.edu
"""

# This performs calculation of the distance
# of the nearest busstop to the area chosen
# It imports pandas module

import pandas as pd
from calc_distance import calc_distance

pd.options.mode.chained_assignment = None

def bus_stop_read(x1, y1, distance=1609.34):
    """
    This method get the bus information from PortAuthority.
    Pick up the bus stops that go to CMU, then
    calculate distance based on a location(latitude and longitude).
    Pick up the surrounding bus stops based on calculated distance,
    and get bus routes such as 71D and 71C.
    """

    # bus route to go to CMU
    cmu_bus_list = ['58', '71B', '71D', '71C', '75', 'P3', '61B', 'v61C', '61A', '61D', '67', '69']

    # setup URL
    url = 'https://data.wprdc.org/dataset/ece64ad3-05eb-46dd-ba38-c83b5373812f/resource/3115c0b9-b48a-49aa-8e39-fd318eb62c04/download/busstopusagebyroute.csv'

    # fetch data with pandas
    csv_data_df = pd.read_csv(url)

    # extract information
    csv_data_df = csv_data_df[['STOP_NAME', 'ROUTE', 'LATITUDE', 'LONGITUDE']]

    # set latitude and longitude for distance calculation
    csv_data_df['base_lati'] = x1
    csv_data_df['base_long'] = y1

    # extract bus route
    csv_data_df = csv_data_df.query('ROUTE in @cmu_bus_list')

    # get latitude and longitude
    point1 = csv_data_df[['base_lati', 'base_long']].values
    point2 = csv_data_df[['LATITUDE', 'LONGITUDE']].values

    # reset index before calculation
    csv_data_df = csv_data_df.reset_index()

    # calculate distance
    csv_data_df['distance'] = calc_distance(point1, point2)

    # check if calculated distance is within the given distance
    csv_data_df = csv_data_df.query('distance < @distance')

    # change m to mile
    csv_data_df['distance'] = csv_data_df['distance'] * 0.000621371

    # capitalize bus stop name
    csv_data_df['STOP_NAME'] = csv_data_df['STOP_NAME'].str.capitalize()

    # return bus stops
    return csv_data_df
