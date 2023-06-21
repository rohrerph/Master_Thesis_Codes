import pandas as pd
import math
from test_env.database_creation.tools import dict, plot
import matplotlib.pyplot as plt
import numpy as np
def calculate(heatingvalue, air_density, flight_vel, savefig, folder_path):
    #load dictionaries
    airplanes_dict = dict.aircraftdata().get_aircraftsfromdatabase()
    airplanes = airplanes_dict.keys()

    #test file to create a dataset using the aircraft-database website. Useful to get aircraft-engine pairs, but e.g. OEW is pretty much never given.

    models = pd.read_json(r"database_creation\rawdata\aircraft-database\aircraft-types.json")
    models = models.explode('engineModels').reset_index(drop=True)
    models = models.explode('propertyValues').reset_index(drop=True)
    manufacturers = pd.read_json(r'database_creation\rawdata\aircraft-database\manufacturers.json')
    manufacturers = manufacturers[['id', 'name']]
    engines = pd.read_json(r"database_creation\rawdata\aircraft-database\engine-models.json")
    engines = engines.explode('propertyValues').reset_index(drop=True)
    properties = pd.read_json(r"database_creation\rawdata\aircraft-database\properties.json")
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
                  'Mmo,float,None',
                  'Maximum operating altitude,integer,foot',
                  'OEW,integer,kilogram',
                  'Wing area,float,square-metre',
                  'Wingspan (canard),float,metre',
                  'Wingspan (winglets),float,metre',
                  'Wingspan,float,metre','Height,float,metre']
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
           'Fan diameter,float,metre', 'Height,float,metre']
    models2 = models2[parameters]
    models3 = models2.loc[models2['name_x_x'].isin(airplanes)]
    models3['name_x_x'] = models3['name_x_x'].map(airplanes_dict)
    models3['Wingspan (winglets),float,metre'].fillna(models3['Wingspan,float,metre'], inplace=True)
    models3['Wingspan,float,metre'] = models3['Wingspan (winglets),float,metre']
    models3 = models3.drop(columns='Wingspan (winglets),float,metre')
    icao = pd.read_excel(r'database_creation\rawdata\emissions\icao_cruise_emissions.xlsx')
    icao = icao[['Engine Identification', 'TSFC Cruise', 'Final Test Date', 'B/P Ratio', 'Pressure Ratio', 'TSFC T/O']]
    icao = icao.groupby(['Engine Identification'], as_index=False).agg({'TSFC T/O':'mean','TSFC Cruise':'mean', 'Final Test Date':'min', 'B/P Ratio':'mean', 'Pressure Ratio':'mean'})

    #MATCH ENGINE MODELS DIRECTLY ON THE EXACT MODEL
    models4 = models3.merge(icao, left_on='name_x_y', right_on='Engine Identification', how='inner')

    #MATCH MODELS BY REPLACING THE SPECIFIC SUBVERSION WITH THE BASIC VERSION
    unmatched = models3.merge(icao, left_on='name_x_y', right_on='Engine Identification', how='left')
    unmatched = unmatched[unmatched['Engine Identification'].isna()]
    unmatched = unmatched.drop(columns= ['Engine Identification', 'TSFC Cruise', 'Final Test Date', 'B/P Ratio', 'Pressure Ratio', 'TSFC T/O'])
    unmatched['name_x_y'] = unmatched['name_x_y'].str.replace(r'/.*', '').str.replace('RB211 ', '')
    mask = icao['Engine Identification'].str.contains('|'.join(unmatched['name_x_y']))
    substring_matches = icao.loc[mask, 'Engine Identification'].str.extract(f'({"|".join(unmatched["name_x_y"])})')
    icao.loc[mask, 'Engine Identification'] = substring_matches[0]
    icao = icao.groupby(['Engine Identification'], as_index=False).agg({'TSFC T/O':'mean','TSFC Cruise':'mean', 'Final Test Date':'min', 'B/P Ratio':'mean', 'Pressure Ratio':'mean'})
    models4b = pd.merge(unmatched, icao, left_on='name_x_y', how='inner', right_on='Engine Identification')
    models4 = models4.append(models4b)

    #MERGE ON ENGINE FAMILIES WITHOUT SUBVERSIONS Specially for JT8D and RB211 and JT3D
    unmatched = pd.merge(unmatched, icao, left_on='name_x_y', how='left', right_on='Engine Identification')
    unmatched = unmatched[unmatched['Engine Identification'].isna()]
    unmatched = unmatched.drop(columns=['Engine Identification', 'TSFC Cruise', 'Final Test Date', 'B/P Ratio', 'Pressure Ratio', 'TSFC T/O'])
    mask = unmatched['name_x_y'].str.contains('RB211', case=False)
    unmatched.loc[mask, 'name_x_y'] = unmatched.loc[mask, 'name_x_y'].str.split('-', n=2).str[:2].str.join('-').str.replace(r'\d+$', '')
    mask = unmatched['name_x_y'].str.contains('LEAP-1', case=False)
    unmatched.loc[mask, 'name_x_y'] = unmatched.loc[mask, 'name_x_y'].str[:-1]
    mask = unmatched['name_x_y'].str.contains('JT3D', case=False)
    unmatched.loc[mask, 'name_x_y'] = 'JT3D-3'
    mask = unmatched['name_x_y'].str.contains('GEnx-1B70', case=False)
    unmatched.loc[mask, 'name_x_y'] = unmatched.loc[mask, 'name_x_y'].str[:-1]
    mask = unmatched['name_x_y'].str.contains('CFM56-3', case=False)
    unmatched.loc[mask, 'name_x_y'] = unmatched.loc[mask, 'name_x_y'].str[:-1]
    unmatched.loc[unmatched['name_x_y'].isin(['JT8D-7A', 'JT8D-9A','JT8D-7B', 'JT8D-9B']), 'name_x_y'] = unmatched.loc[unmatched['name_x_y'].isin(['JT8D-7A', 'JT8D-9A','JT8D-7B', 'JT8D-9B']), 'name_x_y'].str.replace('[AB]$', '')
    mask = icao['Engine Identification'].str.contains('|'.join(unmatched['name_x_y']))
    substring_matches = icao.loc[mask, 'Engine Identification'].str.extract(f'({"|".join(unmatched["name_x_y"])})')
    icao.loc[mask, 'Engine Identification'] = substring_matches[0]
    icao = icao.groupby(['Engine Identification'], as_index=False).agg({'TSFC T/O':'mean','TSFC Cruise':'mean', 'Final Test Date':'min', 'B/P Ratio':'mean', 'Pressure Ratio':'mean'})
    models4c = pd.merge(unmatched, icao, left_on='name_x_y', how='inner', right_on='Engine Identification')

    models4 = models4.append(models4c)

    # Further methods can be integrated to achieve a higher matching rate.
    unmatched = pd.merge(unmatched, icao, left_on='name_x_y', how='left', right_on='Engine Identification')
    unmatched = unmatched[unmatched['Engine Identification'].isna()]
    unmatched = unmatched.drop(columns=['Engine Identification', 'TSFC Cruise', 'Final Test Date', 'B/P Ratio', 'Pressure Ratio', 'TSFC T/O'])

    matchingrate =((len(models4)/len(models3))*100)
    matchingrate = round(matchingrate, 2)
    print(' --> [MATCH ENGINES WITH ICAO EMISSION DATABANK]: Matching Rate: ' + str(matchingrate) + ' %')
    models4['Air Mass Flow [kg/s]'] = (air_density* flight_vel * math.pi * models4['Fan diameter,float,metre']**2)/4
    models4['Engine Efficiency'] = flight_vel / (heatingvalue * models4['TSFC Cruise'])
    databank = pd.read_excel(r'Databank.xlsx')
    #databank = databank.groupby(['Company','Name', 'YOI', 'Type'], as_index=False).agg({'OEW': 'mean', 'Exit Limit':'mean','MTOW':'max', 'EU (MJ/ASK)':'mean', 'Fuel Flow [kg/s]':'mean'})
    databank['Name'] = databank['Name'].str.strip()
    models4['name_x_x'] = models4['name_x_x'].str.strip()
    databank = pd.merge(models4, databank, left_on='name_x_x', right_on='Name', how='outer')
    databank = databank.drop(columns=['name_y_x', 'name_x_x', 'name_x_y','name_y_y'])
    aircraft_database = pd.read_excel(r'database_creation\rawdata\aircraftproperties\Aircraft Databank v2.xlsx', sheet_name='New Data Entry')
    aircraft_database = aircraft_database.dropna(subset='TSFC (mg/Ns)')
    aircraft_database = aircraft_database.groupby(['Name','YOI'], as_index=False).agg({'TSFC (mg/Ns)':'mean'})
    aircraft_database['TSFC Cruise'] =aircraft_database['TSFC (mg/Ns)']
    use_lee_et_al = True
    if use_lee_et_al:
        for index, row in aircraft_database.iterrows():
            name = row['Name']
            value = row['TSFC Cruise']

            # update corresponding row in df2 with the value from df1
            databank.loc[databank['Name'] == name, 'TSFC Cruise'] = value
            databank['Engine Efficiency'] = flight_vel / (heatingvalue * databank['TSFC Cruise'])
    databank.to_excel(r'Databank.xlsx', index=False)

    #PLOT engine efficiency
    fig = plt.figure(dpi=300)
    ax = fig.add_subplot(1, 1, 1)
    years = np.arange(1955, 2023)
    x_all = databank['YOI'].astype(np.int64)
    y_all = databank['TSFC Cruise'].astype(np.float64)
    z_all = np.polyfit(x_all,  y_all, 2)
    p_all = np.poly1d(z_all)

    #  Limits from Kurzke
    limit = (0.555 * heatingvalue / flight_vel)**-1
    limit_nox = (0.50875 * heatingvalue / flight_vel) ** -1

    bpr = databank.groupby(['Name', 'YOI'], as_index=False).agg({'TSFC Cruise': 'mean',  'B/P Ratio': 'mean', 'Pressure Ratio':'mean'})
    low = bpr.loc[bpr['B/P Ratio'] <= 2]
    medium = bpr.loc[(bpr['B/P Ratio'] >= 2) & (bpr['B/P Ratio'] <= 8)]
    high = bpr.loc[bpr['B/P Ratio'] >= 8]

    ax.scatter(low['YOI'], low['TSFC Cruise'], color='red', label='BPR <2')
    ax.scatter(medium['YOI'], medium['TSFC Cruise'], color='purple', label='BPR 2-8')
    ax.scatter(high['YOI'], high['TSFC Cruise'], color='blue', label='BPR >8')

    ax.axhline(y=limit_nox, color='black', linestyle='--', linewidth=2, label='Practical Limit w.r.t. NOx')
    ax.axhline(y=limit, color='black', linestyle='-', linewidth=2, label = 'Theoretical Limit')

    # Fuse in Data for Future projections
    #ax.scatter(2020, 13.736, color='green')
    #plt.annotate('Advanced Turbofan', (2020, 13.736),
                    #fontsize=6, xytext=(-10, 5),
                    #textcoords='offset points')
    ax.scatter(2020, 14.94, color='green', label='Future Projections')
    plt.annotate('GE9X', (2020, 14.94),
                    fontsize=6, xytext=(-10, -10),
                    textcoords='offset points')
    ax.scatter(2025, 12.88, color='green')
    plt.annotate('Ultrafan', (2025, 12.88),
                    fontsize=6, xytext=(-10, 5),
                    textcoords='offset points')
    ax.scatter(2030, 12.152, color='green')
    plt.annotate('Open Rotor', (2030, 12.152),
                    fontsize=6, xytext=(-10, 5),
                    textcoords='offset points')
    ax.scatter(2035, 12, color='green')
    plt.annotate('CFM RISE', (2035, 12),
                    fontsize=6, xytext=(-10, -10),
                    textcoords='offset points')
    plt.xlim(1955,2050)


    ax.legend()
    xlabel = 'Aircraft Year of Introduction'
    ylabel = 'Cruise TSFC [g/kNs]'
    plot.plot_layout(None, xlabel, ylabel, ax)
    if savefig:
        plt.savefig(folder_path+'\engineefficiency.png')

    # PLOT colors for OPR
    fig = plt.figure(dpi=300)
    ax = fig.add_subplot(1, 1, 1)

    low = bpr.loc[bpr['Pressure Ratio'] <= 20]
    medium = bpr.loc[(bpr['Pressure Ratio'] >= 20) & (bpr['Pressure Ratio'] <= 35)]
    high = bpr.loc[bpr['Pressure Ratio'] >= 35]

    ax.scatter(low['YOI'], low['TSFC Cruise'], color='red', label='OPR <20')
    ax.scatter(medium['YOI'], medium['TSFC Cruise'], color='purple', label='OPR 20-35')
    ax.scatter(high['YOI'], high['TSFC Cruise'], color='blue', label='OPR >35')

    ax.axhline(y=limit_nox, color='black', linestyle='--', linewidth=2, label='Practical Limit w.r.t. NOx')
    ax.axhline(y=limit, color='black', linestyle='-', linewidth=2, label = 'Theoretical Limit')

    ax.legend()
    xlabel = 'Aircraft Year of Introduction'
    ylabel = 'Cruise TSFC [g/kNs]'
    plot.plot_layout(None, xlabel, ylabel, ax)
    if savefig:
        plt.savefig(folder_path+'\engineefficiency_opr.png')

    # Create Weight statistics
    fig = plt.figure(dpi=300)
    ax = fig.add_subplot(1, 1, 1)
    databank = databank.loc[databank['Type']!='Regional']
    databank['Dry weight,integer,kilogram'] = databank['Dry weight,integer,kilogram']*databank['engineCount']
    databank['Dry weight,integer,kilogram'] = databank['Dry weight,integer,kilogram'] / databank['OEW']
    databank.to_excel(r"C:\Users\PRohr\Desktop\test.xlsx")
    databank = databank.groupby(['Name', 'YOI'], as_index=False).agg({'Dry weight,integer,kilogram': 'mean',  'B/P Ratio': 'mean'})
    low = databank.loc[databank['B/P Ratio'] <= 2]
    medium = databank.loc[(databank['B/P Ratio'] >= 2) & (databank['B/P Ratio'] <= 8)]
    high = databank.loc[databank['B/P Ratio'] >= 8]

    ax.scatter(low['YOI'], low['Dry weight,integer,kilogram'], color='red', label='BPR <2')
    ax.scatter(medium['YOI'], medium['Dry weight,integer,kilogram'], color='purple', label='BPR 2-8')
    ax.scatter(high['YOI'], high['Dry weight,integer,kilogram'], color='blue', label='BPR >8')
    plt.xlim(1955, 2025)
    plt.ylim(0, 0.2)

    ax.legend()
    title = 'Individual Aircraft'
    xlabel = 'Aircraft Year of Introduction'
    ylabel = 'Engine Weight / OEW'
    plot.plot_layout(title, xlabel, ylabel, ax)
    if savefig:
        plt.savefig(folder_path + '\engineweight.png')


