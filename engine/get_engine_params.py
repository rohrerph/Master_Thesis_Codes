import pandas as pd
import math
from tools import dict

#load dictionaries
fullnames = dict.fullname().get_aircraftfullnames()
airplanes_dict = dict.AirplaneModels().get_models()
aircraftnames = dict.AircraftNames().get_aircraftnames()
airplanes = airplanes_dict.keys()
airlines = dict.USAirlines().get_airlines()

#read all input files
T2 = pd.read_csv(r"C:\Users\PRohr\Desktop\Masterarbeit\Data\T_SCHEDULE_T2.csv")
AC_types = pd.read_csv(r"C:\Users\PRohr\Desktop\Masterarbeit\Python\overall\data\L_AIRCRAFT_TYPE (1).csv")
manufacturers = pd.read_json(r'C:\Users\PRohr\Downloads\manufacturers.json')
engines = pd.read_json(r"C:\Users\PRohr\Downloads\engine-models.json")
aircraft_data = pd.read_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\overall\data\Databank.xlsx')

manufacturers = manufacturers[['id', 'name']]
engines = engines.explode('propertyValues').reset_index(drop=True)
properties = pd.read_json(r"C:\Users\PRohr\Downloads\properties.json")
properties['Value']= properties['name'].astype(str)+','+properties['type'].astype(str)+','+properties['unit'].astype(str)
properties = properties[['id', 'Value']]
properties_dict = properties.set_index('id')['Value'].to_dict()
all_engines = pd.json_normalize(engines['propertyValues'])

engines = pd.concat([engines, all_engines.reindex(engines.index)], axis=1)
engines = engines.replace(properties_dict)
engines2 = engines.pivot(columns='property',values='value')
engines = engines.join(engines2)
engines = engines.loc[engines['engineFamily'].isin(['turbofan','turboprop'])]
#sort for relevant entries:
parameters= ['id',
             'engineFamily',
             'manufacturer',
             'name',
             'Bypass ratio,float,None',
             'Compression ratio,float,None',
             'Compressor stages,integer,None',
             'Cooling system,string,None',
             'Dry weight,integer,kilogram',
             'Fan blades,integer,None',
             'Fan diameter,float,metre',
             'Max. continuous power,integer,kilowatt',
             'Overall pressure ratio,float,None',
             'Max. continuous thrust,float,kilonewton']
engines = engines[parameters]
engines_grouped = engines.groupby(['name', 'id','engineFamily','manufacturer'], as_index=False).mean()
engines_grouped = engines_grouped.merge(manufacturers, left_on='manufacturer',right_on='id')
engines_grouped = engines_grouped.drop(columns=['id_y','manufacturer'])

#swap engines name that the databank recognizes it.

substitutes = {'Trent7000-72':'Trent 7000-72', 'Tay Mk 620-15':'Tay 620-15', 'BR715-A1-30':'715A1-30','BR715-C1-30':'715C1-30' }
aircraft_data['Engine'] = aircraft_data['Engine'].replace(substitutes)
ind_engines = aircraft_data['Engine'].drop_duplicates(keep='first').dropna()
engine_list = list(ind_engines)

grouped = pd.DataFrame(columns=['Engine', 'B/P Ratio', 'Pressure Ratio',
                                'Fan diameter'])
for engine in engine_list:
    # Create a boolean mask for rows that contain the current substring
    mask = engines_grouped['name_x'].str.contains(engine)

    # Sum the 'value_column' for rows that match the mask
    family = engines_grouped.loc[mask, 'engineFamily']
    bpratio = engines_grouped.loc[mask, 'Bypass ratio,float,None'].mean()
    pressureratio = engines_grouped.loc[mask, 'Overall pressure ratio,float,None'].mean()
    fandiameter = engines_grouped.loc[mask, 'Fan diameter,float,metre'].mean()

    # Append the substring and the sum to the results dataframe
    grouped = grouped.append({'Engine': engine,
                              'Engine Family':family,
                              'B/P Ratio': bpratio,
                              'Pressure Ratio': pressureratio,
                              'Fan diameter': fandiameter}, ignore_index=True)

swap_substitutes_back = {value: key for key, value in substitutes.items()}
grouped['Engine'] = grouped['Engine'].replace(swap_substitutes_back)

aircraft_data = aircraft_data.merge(grouped[['Engine','Fan diameter']], on='Engine', how='left')

#calculate the air mass flow, using basic conditions using a cruise speed of 240 m/s and an air density of 0.4135 in 10 km height.
air_density = 0.4135 #kg/m^3
speed = 240 #m/s
aircraft_data['Air Mass Flow [kg/s]'] = (air_density* speed* math.pi * aircraft_data['Fan diameter']**2)/4


aircraft_data.to_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\overall\data\Databank.xlsx', index=False)



