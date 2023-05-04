import pandas as pd
import math
from test_env.tools import dict

def calculate(air_density,flight_vel):
    #load dictionaries
    airplanes_dict = dict.aircraftdata().get_aircraftsfromdatabase()
    airplanes = airplanes_dict.keys()

    #test file to create a dataset using the aircraft-database website. Useful to get aircraft-engine pairs, but e.g. OEW is pretty much never given.

    models = pd.read_json(r"C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\database_creation\rawdata\aircraft-database\aircraft-types.json")
    models = models.explode('engineModels').reset_index(drop=True)
    models = models.explode('propertyValues').reset_index(drop=True)
    manufacturers = pd.read_json(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\database_creation\rawdata\aircraft-database\manufacturers.json')
    manufacturers = manufacturers[['id', 'name']]
    engines = pd.read_json(r"C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\database_creation\rawdata\aircraft-database\engine-models.json")
    engines = engines.explode('propertyValues').reset_index(drop=True)
    properties = pd.read_json(r"C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\database_creation\rawdata\aircraft-database\properties.json")
    properties['Value']= properties['name'].astype(str)+','+properties['type'].astype(str)+','+properties['unit'].astype(str)
    properties = properties[['id', 'Value']]
    properties_dict = properties.set_index('id')['Value'].to_dict()
    models_properties = pd.json_normalize(models['propertyValues'])
    models = models.join(models_properties)


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
                 'Dry weight,integer,kilogram',
                 'Bypass ratio,float,None',
                 'Compression ratio,float,None',
                 'Compressor stages,integer,None',
                 'Cooling system,string,None',
                 'Fan blades,integer,None',
                 'Fan diameter,float,metre',
                 'Max. continuous power,integer,kilowatt',
                 'Overall pressure ratio,float,None',
                 'Max. continuous thrust,float,kilonewton']
    engines = engines[parameters]
    engines_grouped = engines.groupby(['name', 'id','engineFamily','manufacturer'], as_index=False).mean()
    engines_grouped = engines_grouped.merge(manufacturers, left_on='manufacturer',right_on='id')
    engines_grouped = engines_grouped.drop(columns=['id_y','manufacturer'])

    #engines_grouped.to_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\other\output\engines_fan_diameter.xlsx')

    models = models.merge(manufacturers, left_on='manufacturer', right_on='id')
    models = models.replace(properties_dict)
    models2 = models.pivot(columns='property',values='value')
    models = models.join(models2)
    parameters = ['id_x',
                  'name_x',
                  'engineModels',
                  'name_y',
                  'engineCount',
                  'Fuel capacity,integer,litre',
                  'MLW,integer,kilogram',
                  'MTOW,integer,kilogram',
                  'MTW,integer,kilogram',
                  'MZFW,integer,kilogram',
                  'Ma,float,None',
                  'Maximum operating altitude,integer,foot',
                  'OEW,integer,kilogram',
                  'Wing area,float,square-metre',
                  'Wingspan (canard),float,metre',
                  'Wingspan (winglets),float,metre',
                  'Wingspan,float,metre']
    models = models[parameters]
    models_grouped = models.groupby(['id_x','name_x', 'engineModels','name_y', 'engineCount'], as_index=False).mean()

    models2 = models_grouped.merge(engines_grouped, left_on='engineModels', right_on='id_x')
    parameters = ['name_x_x', 'name_y_x', 'engineCount',
           'Fuel capacity,integer,litre', 'MLW,integer,kilogram',
           'MTOW,integer,kilogram', 'MTW,integer,kilogram',
           'MZFW,integer,kilogram',
           'Maximum operating altitude,integer,foot',
           'Wing area,float,square-metre',
           'Wingspan,float,metre','Wingspan (winglets),float,metre', 'name_x_y','name_y_y',
            'engineFamily', 'Bypass ratio,float,None', 'Overall pressure ratio,float,None',
           'Dry weight,integer,kilogram',
           'Fan diameter,float,metre']
    models2 = models2[parameters]
    models3 = models2.loc[models2['name_x_x'].isin(airplanes)]
    models3['name_x_x'] = models3['name_x_x'].map(airplanes_dict)
    models3['Wingspan (winglets),float,metre'].fillna(models3['Wingspan,float,metre'], inplace=True)
    models3['Wingspan,float,metre'] = models3['Wingspan (winglets),float,metre']
    models3 = models3.drop(columns='Wingspan (winglets),float,metre')
    icao = pd.read_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\database_creation\rawdata\emissions\icao_cruise_emissions.xlsx')
    icao = icao[['Engine Identification', 'TSFC Cruise', 'Final Test Date', 'B/P Ratio', 'Pressure Ratio', 'TSFC T/O']]
    icao = icao.groupby(['Engine Identification'], as_index=False).agg({'TSFC T/O':'mean','TSFC Cruise':'mean', 'Final Test Date':'min', 'B/P Ratio':'mean', 'Pressure Ratio':'mean'})
    models4 = models3.merge(icao, left_on='name_x_y', right_on='Engine Identification')
    models4.to_excel(r'C:\Users\PRohr\Desktop\test.xlsx')
    matchingrate =((len(models4)/len(models3))*100)
    matchingrate = round(matchingrate, 2)
    print(' --> [MATCH ENGINES WITH ICAO EMISSION DATABANK]: Matching Rate: ' + str(matchingrate) + ' %')
    models4['Air Mass Flow [kg/s]'] = (air_density* flight_vel * math.pi * models4['Fan diameter,float,metre']**2)/4
    heatingvalue = 43.1  # MJ/kg
    models4['Engine Efficiency'] = flight_vel / (heatingvalue * models4['TSFC Cruise'])
    databank = pd.read_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\Databank.xlsx')
    #databank = databank.groupby(['Company','Name', 'YOI', 'Type'], as_index=False).agg({'OEW': 'mean', 'Exit Limit':'mean','MTOW':'max', 'EU (MJ/ASK)':'mean', 'Fuel Flow [kg/s]':'mean'})
    databank['Name'] = databank['Name'].str.strip()
    models4['name_x_x'] = models4['name_x_x'].str.strip()
    databank = pd.merge(models4, databank, left_on='name_x_x', right_on='Name', how='left')
    databank = databank.drop(columns=['name_y_x', 'name_x_x', 'name_x_y','name_y_y'])

    databank.to_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\Databank.xlsx', index=False)