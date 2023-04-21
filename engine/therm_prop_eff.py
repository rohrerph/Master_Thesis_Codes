import pandas as pd
import numpy as np
from tools import dict
from tools import T2_preprocessing
import math
import matplotlib.pyplot as plt

#load dictionaries
fullnames = dict.fullname().get_aircraftfullnames()
airplanes_dict = dict.AirplaneModels().get_models()
aircraftnames = dict.AircraftNames().get_aircraftnames()
airplanes = airplanes_dict.keys()
airlines = dict.USAirlines().get_airlines()

#get avrg fuel flow:
T2 = pd.read_csv(r"C:\Users\PRohr\Desktop\Masterarbeit\Data\T_SCHEDULE_T2.csv")
AC_types = pd.read_csv(r"C:\Users\PRohr\Desktop\Masterarbeit\Data\L_AIRCRAFT_TYPE (1).csv")
T2 = T2_preprocessing.preprocessing(T2, AC_types, airlines, airplanes)
gallon = 3.7854 #liter
T2['Fuel Flow [kg/s]']= (T2['AIRCRAFT_FUELS_921']*gallon)/(T2['HOURS_AIRBORNE_650']*3600)
T2.replace([np.inf, - np.inf], np.nan, inplace = True)
T2 = T2.dropna(subset=['Fuel Flow [kg/s]'])
AC_type = T2.groupby(['Description'], as_index=False).agg({'Fuel Flow [kg/s]':'mean'})
AC_type['Description'] = AC_type['Description'].replace(fullnames)

#Merge with my database to get engines

aircraft_data = pd.read_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\overall\data\Aircraft Databank v2.xlsx',sheet_name='New Data Entry')


def get_icao_params(aircraft_data):
    substitutes = dict.Substitutes().engine_substitute()
    path = r'C:\Users\PRohr\Desktop\Masterarbeit\Python\engine\output\icao_cruise_emissions.xlsx'
    icao_emissions = pd.read_excel(path)
    aircraft_data = aircraft_data.loc[aircraft_data['Check'] == 'Yes']
    aircraft_data['Engine'] = aircraft_data['Engine'].replace(substitutes)
    ind_engines = aircraft_data.drop_duplicates(subset='Engine')
    engine_list = list(ind_engines['Engine'])
    # Create an empty dataframe to store the results
    grouped = pd.DataFrame(columns=['Engine',  'Final Test Date', 'B/P Ratio', 'Pressure Ratio',
           'Rated Thrust (kN)', 'TSFC Cruise'])

    # Loop over the substrings and group the dataframe for each one
    for engine in engine_list:
        # Create a boolean mask for rows that contain the current substring
        mask = icao_emissions['Engine Identification'].str.contains(engine)

        # Sum the 'value_column' for rows that match the mask
        tsfc_cruise = icao_emissions.loc[mask, 'TSFC Cruise'].mean()
        testdate = icao_emissions.loc[mask, 'Final Test Date'].min()
        bpratio = icao_emissions.loc[mask,'B/P Ratio'].mean()
        pressureratio = icao_emissions.loc[mask, 'Pressure Ratio'].mean()
        thrust = icao_emissions.loc[mask, 'Rated Thrust (kN)'].mean()

        # Append the substring and the sum to the results dataframe
        grouped = grouped.append({'Engine': engine,
                                  'TSFC Cruise': tsfc_cruise,
                                  'Final Test Date':testdate,
                                  'B/P Ratio': bpratio,
                                  'Pressure Ratio': pressureratio,
                                  'Rated Thrust (kN)': thrust}, ignore_index=True)

    grouped_nan = grouped[grouped['TSFC Cruise'].isna()]
    grouped_notna = grouped[~grouped['TSFC Cruise'].isna()]

    #5 engines cant be assigned a value from the icao emissions df
    grouped_nan_2 = pd.merge(grouped_nan, aircraft_data[['Engine','Engine TSFC cruise [g/kNs]']])
    grouped_nan_2['TSFC Cruise']= grouped_nan_2['Engine TSFC cruise [g/kNs]']
    grouped_nan_2 = grouped_nan_2.drop('Engine TSFC cruise [g/kNs]', axis=1)

    grouped = grouped_notna.append(grouped_nan_2)

    #grouped = grouped.dropna(subset='Final Test Date').reset_index()
    all = grouped
    return all

all = get_icao_params(aircraft_data)


data = pd.merge(all, aircraft_data, left_on='Engine', right_on='Engine')
data['Name'] = data['Name'].str.strip()
data = pd.merge(data, AC_type, left_on='Name', right_on='Description')
data = data[['Company', 'Name','Engine', 'YOI','MTOW', 'B/P Ratio', 'Pressure Ratio', 'Rated Thrust (kN)', 'TSFC Cruise', 'Fuel Flow [kg/s]']]
data['Thrust assumption'] = (9.81*data['MTOW'])/15
engines_fan_diameter = pd.read_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\other\output\engines_fan_diameter.xlsx')
engines_fan_diameter = engines_fan_diameter[['name_x', 'Fan diameter,float,metre', 'Max. continuous thrust,float,kilonewton']]

data = pd.merge(data, engines_fan_diameter, left_on='Engine', right_on='name_x')

flight_speed = 240 #m/s
rho = 0.4135
mach = 0.8
altitude = 10000 #m
heating_value = 42.8 #MJ/kg

data['Fan area'] = math.pi * data['Fan diameter,float,metre']**2 /4
data['Air mass flow [kg/s]'] = data['Fan area']*rho*flight_speed

#use metric from the book Aircraft Propulsion and Gas Turbine Engines
data['Air Mass Core'] = data['Air mass flow [kg/s]']/data['B/P Ratio']
data['Air Mass Fan'] = data['Air mass flow [kg/s]'] - data['Air Mass Core']
data['f'] = data['Fuel Flow [kg/s]']/data['Air mass flow [kg/s]']
data['Velocity Fan'] = (0.75*data['Thrust assumption'])/data['Air Mass Fan'] + flight_speed
data['Velocity Core'] = ((0.25*data['Thrust assumption']/data['Air Mass Core']) + flight_speed) / (1+data['f'])

data['nominator']= 2*flight_speed*(((data['f']+1)*data['Velocity Core']-flight_speed) + data['B/P Ratio']*(data['Velocity Fan']-flight_speed))
data['denominator']= ((1+data['f'])*data['Velocity Core']**2-flight_speed**2)+data['B/P Ratio']*(data['Velocity Fan']**2-flight_speed**2)
data['prop_eff'] = data['nominator']/data['denominator']

data['nominator_thermal']= data['Air Mass Core']*((1+data['f'])*data['Velocity Core']**2-flight_speed**2)+data['Air Mass Fan']*(data['Velocity Fan']**2-flight_speed**2)
data['denominator_thermal'] = (2*data['Fuel Flow [kg/s]']*42.8*10**6)
data['thermal_eff'] = data['nominator_thermal']/data['denominator_thermal']
data['ovr_eff'] = flight_speed / (data['TSFC Cruise']* heating_value)
data['ovr_eff_calc'] = data['thermal_eff']*data['prop_eff']
data = data.groupby(['Name', 'Engine'], as_index=False).agg({'thermal_eff':'mean', 'prop_eff':'mean', 'ovr_eff':'mean', 'ovr_eff_calc':'mean'})
#more or less accurate values when we half the max continuous thrust, how much continuous thrust is used for steady cruise. ?

