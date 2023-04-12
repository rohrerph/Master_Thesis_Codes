import pandas as pd
import os
import numpy as np
from tools import dict
from tools import plot
from tools import T2_preprocessing
import matplotlib.pyplot as plt

#load dictionaries
airplanes_dict = dict.AirplaneModels().get_models()
aircraftnames = dict.AircraftNames().get_aircraftnames()
airplanes = airplanes_dict.keys()
airlines = dict.USAirlines().get_airlines()


# Create an empty dataframe to hold the data
T100 = pd.DataFrame()

# Get a list of all files in the folder
folder_path = r"C:\Users\PRohr\Desktop\Masterarbeit\Data\T100_Annual"
file_list = os.listdir(folder_path)

# Loop through each file and read it into a dataframe, and append to the combined dataframe
for file_name in file_list:
    file_path = os.path.join(folder_path, file_name)
    df = pd.read_csv(file_path)
    T100 = T100.append(df, ignore_index=True)

#Data from December 2022, is also monthly available back to 1990.
AC_types = pd.read_csv(r"C:\Users\PRohr\Desktop\Masterarbeit\Data\L_AIRCRAFT_TYPE (1).csv")

T100 = T100.loc[T100['CARRIER_GROUP'] == 3]
# subgroup 1 for aircraft passenger configuration
T100 = T100.loc[T100['AIRCRAFT_CONFIG'] == 1]
# Use the 19 Airlines
T100 = T100.loc[T100['UNIQUE_CARRIER_NAME'].isin(airlines)]
T100 = pd.merge(T100, AC_types, left_on='AIRCRAFT_TYPE', right_on='Code')
T100 = T100.loc[T100['Description'].isin(airplanes)]
T100 = T100.loc[T100['SEATS']>0]
average_seats = T100.groupby(['Description', 'UNIQUE_CARRIER_NAME'], as_index=False).agg({'SEATS':'sum', 'DEPARTURES_PERFORMED':'sum'})
average_seats['Average Seats']=average_seats['SEATS']/average_seats['DEPARTURES_PERFORMED']
average_seats['Average Seats'] = average_seats['Average Seats'].round(0)
average_seats = average_seats[['Description', 'Average Seats']]
average_seats = average_seats.groupby(['Description'], as_index=False).agg(['min', 'mean', 'max'])
average_seats = average_seats.round(0)

average_seats.to_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Data\usdot_seats.xlsx')