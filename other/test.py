import pandas as pd
from tools import dict
import json
#test file to create a dataset using the aircraft-database website. Useful to get aircraft-engine pairs, but e.g. OEW is pretty much never given.

models = pd.read_json(r'C:\Users\PRohr\Downloads\aircraft-models.json')

models = pd.read_json(r"C:\Users\PRohr\Downloads\aircraft-types.json")
models = models.explode('engineModels').reset_index(drop=True)
models = models.explode('propertyValues').reset_index(drop=True)
manufacturers = pd.read_json(r'C:\Users\PRohr\Downloads\manufacturers.json')
manufacturers = manufacturers[['id', 'name']]
engines = pd.read_json(r"C:\Users\PRohr\Downloads\engine-models.json")
engines = engines.explode('propertyValues').reset_index(drop=True)
properties = pd.read_json(r"C:\Users\PRohr\Downloads\properties.json")
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
engines = engines.loc[engines['engineFamily']=='turbofan']
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

engines_grouped.to_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\other\output\engines_fan_diameter.xlsx')

models = models.merge(manufacturers, left_on='manufacturer', right_on='id')
models = models.replace(properties_dict)
models2 = models.pivot(columns='property',values='value')
models = models.join(models2)
parameters = ['id_x',
              'name_x',
              'engineModels',
              'name_y',
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
models_grouped = models.groupby(['id_x','name_x', 'engineModels','name_y'], as_index=False).mean()

models2 = models_grouped.merge(engines_grouped, left_on='engineModels', right_on='id_x')
parameters = ['name_x_x', 'name_y_x',
       'Fuel capacity,integer,litre', 'MLW,integer,kilogram',
       'MTOW,integer,kilogram', 'MTW,integer,kilogram',
       'MZFW,integer,kilogram',
       'Maximum operating altitude,integer,foot', 'OEW,integer,kilogram',
       'Wing area,float,square-metre',
       'Wingspan (winglets),float,metre', 'Wingspan,float,metre', 'name_x_y','name_y_y',
        'engineFamily', 'Bypass ratio,float,None', 'Overall pressure ratio,float,None',
       'Compression ratio,float,None', 'Compressor stages,integer,None',
       'Dry weight,integer,kilogram', 'Fan blades,integer,None',
       'Fan diameter,float,metre', 'Max. continuous power,integer,kilowatt']
models2 = models2[parameters]

airplanes = ['757-200', '767-300', '777-200', 'A320-100', '767-200', '737-800', 'A319', '737-300', 'DC9', '747-400', '737-700', '727-200', 'A330-200', '767-400', 'DC-10-30', 'A321', '737-400', '737-100', '737-500', '747-200', 'MD-11', '757-300', '737-900', '747-100', 'RJ-700', '787-800', 'DC-9-30',
             'A330-300', 'Embraer-145', '777-300', 'Embraer 190', '787-900', 'DC-10-10', 'L-1011-1', 'A300-600', '737-900ER', 'RJ-200ER', 'MD-90', 'DC-10-40', '717-200', 'ERJ-175', '737 Max 800', '787-10 Dreamliner', 'A330-900', '737 Max 900']

models3 = models2.loc[models2['name_x_x'].isin(airplanes)]
mask = models2['name_x_x'].str.contains('|'.join(airplanes))

models3 = models3.groupby(['name_x_x'], as_index=False).first()
result = models2[mask]
result = result.groupby(['name_x_x'], as_index=False).first()