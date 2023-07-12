import pandas as pd
import math
from test_env.database_creation.tools import plot
import numpy as np
import matplotlib.pyplot as plt

def calculate(savefig, air_density,flight_vel, g, folder_path):
    aircraft_data = pd.read_excel(r'Databank.xlsx')
    lift_data = pd.read_excel(r'database_creation\rawdata\aircraftproperties\Aicrraft Range Data Extraction.xlsx', sheet_name='2. Table')
    # Remove these Regional jets, it seems, that their data is not accurate, possibly because overall all values are much smaller.
    lift_data = lift_data[~lift_data['Name'].isin(['RJ-200ER /RJ-440', 'RJ-700', 'Embraer ERJ-175', 'Embraer-145', 'Embraer-135', 'Embraer 190'])]
    aircraft_data = aircraft_data.merge(lift_data, on='Name', how='left')

    # factor Beta which accounts for the weight fraction burnt in non cruise phase
    # Martinez et al. used a factor of 0.9 to 0.93 but probably it is better to subtract a certain weight.
    #optimize factor for minimal R-squared between K1 and K2 ?

    beta = lambda x: 0.96 if x == 'Wide' else(0.94 if x =='Narrow' else 0.88)

    aircraft_data['Factor'] = aircraft_data['Type'].apply(beta)
    aircraft_data['Ratio 1']= aircraft_data['Factor']*aircraft_data["MTOW\n(Kg)"]/aircraft_data['MZFW_POINT_1\n(Kg)']
    aircraft_data['Ratio 2']= aircraft_data['Factor']*aircraft_data["MTOW\n(Kg)"]/aircraft_data['MZFW_POINT_2\n(Kg)']

    breguet = aircraft_data

    breguet['Ratio 1']=breguet['Ratio 1'].apply(np.log)
    breguet['Ratio 2']=breguet['Ratio 2'].apply(np.log)

    breguet['K_1']= breguet['RANGE_POINT_1\n(Km)']/breguet['Ratio 1']
    breguet['K_2']= breguet['RANGE_POINT_2\n(Km)']/breguet['Ratio 2']
    breguet['K']=(breguet['K_1']+breguet['K_2'])/2
    comet_k1 = 5190 / (np.log(0.94*73480/43410)) # data for the Comet 4 from Aerospaceweb.org
    breguet.loc[breguet['Name'] == 'Comet 4', 'K_1'] = comet_k1

    breguet['A'] = breguet['K_1']*g*0.001*breguet['TSFC Cruise']
    breguet['L/D estimate'] = breguet['A']/flight_vel
    comet_A = breguet.loc[breguet['Name'] == 'Comet 4', 'A']
    breguet.loc[breguet['Name'] == 'Comet 4', 'L/D estimate'] = comet_A/223.6 # account for lower speed of the Comet 4
    aircraft_data = breguet
    aircraft_data = aircraft_data.drop(columns=['#', 'Aircraft Model Chart', 'Link', 'Factor', 'Ratio 1',
           'Ratio 2', 'K_1', 'K_2', 'K', 'A'])
    aircraft_data['Dmax'] = (g * aircraft_data['MTOW\n(Kg)']) / aircraft_data['L/D estimate']
    aircraft_data['Aspect Ratio'] = aircraft_data['Wingspan,float,metre']**2/aircraft_data['Wing area,float,square-metre']
    aircraft_data['c_L'] = (2* g * aircraft_data['MTOW\n(Kg)']) / (air_density*(flight_vel**2)*aircraft_data['Wing area,float,square-metre'])
    aircraft_data['c_D'] = aircraft_data['c_L'] / aircraft_data['L/D estimate']
    aircraft_data['k'] = 1 / (math.pi * aircraft_data['Aspect Ratio'] * 0.8)
    aircraft_data['c_Di'] = aircraft_data['k']*(aircraft_data['c_L']**2)
    aircraft_data['c_D0'] = aircraft_data['c_D']-aircraft_data['c_Di']
    aircraft_database = pd.read_excel(r'database_creation\rawdata\aircraftproperties\Aircraft Databank v2.xlsx', sheet_name='New Data Entry')
    aircraft_database = aircraft_database.dropna(subset='L/Dmax')
    aircraft_database = aircraft_database.groupby(['Name','YOI'], as_index=False).agg({'L/Dmax':'mean'})
    aircraft_database['L/D estimate'] =aircraft_database['L/Dmax']
    use_lee_et_al = True
    if use_lee_et_al:
        for index, row in aircraft_database.iterrows():
            name = row['Name']
            value = row['L/D estimate']

            # update corresponding row in df2 with the value from df1
            aircraft_data.loc[aircraft_data['Name'] == name, 'L/D estimate'] = value

    aircraft_data['EU_estimate1'] = (43.1 * (aircraft_data['MTOW\n(Kg)'] - aircraft_data['MZFW_POINT_1\n(Kg)']))/(aircraft_data['Pax']*aircraft_data['RANGE_POINT_1\n(Km)'])
    aircraft_data['EU_estimate2'] = (43.1 * (aircraft_data['MTOW\n(Kg)'] - aircraft_data['MZFW_POINT_2\n(Kg)'])) / (aircraft_data['Pax'] * aircraft_data['RANGE_POINT_2\n(Km)'])
    aircraft_data['EU_estimate'] = (aircraft_data['EU_estimate1']+aircraft_data['EU_estimate2'])/2

    aircraft_data = aircraft_data.drop(columns=['MTOW\n(Kg)', 'MZFW_POINT_1\n(Kg)', 'RANGE_POINT_1\n(Km)', 'MZFW_POINT_2\n(Kg)', 'RANGE_POINT_2\n(Km)', 'EU_estimate1', 'EU_estimate2'])
    aircraft_data.to_excel(r'Databank.xlsx', index=False)

    breguet = aircraft_data.dropna(subset='L/D estimate')
    breguet = breguet.groupby(['Name', 'YOI', 'Type'], as_index=False).agg({'L/D estimate':'mean'})
    wide = breguet.loc[breguet['Type']=='Wide']
    narrow = breguet.loc[breguet['Type'] != 'Wide']
    # Use value for 737-900 also for the ER version
    b737 = narrow.loc[narrow['Name'] == '737-900', 'L/D estimate'].values[0]
    narrow.loc[narrow['Name'] == '737-900ER', 'L/D estimate'] = b737
    # Get Referenced Aircraft
    a350 = wide.loc[wide['Name'] == 'A350-900', 'L/D estimate'].iloc[0]
    a340 = wide.loc[wide['Name'] == 'A340-500', 'L/D estimate'].iloc[0]
    a321 = narrow.loc[narrow['Name'] == 'A321-200n', 'L/D estimate'].iloc[0]
    limit = a350 * 1.05 * 1.15
    # assume 40% is induced drag for the A321 which can be reduced by the AlbatrossOne wingspan. Induced drag can be scaled by the squareroot of the ARs
    factor = np.sqrt(10.47/18)*0.4+0.6



    # Create subplots for each column
    cm = 1 / 2.54  # for inches-cm conversion
    fig = plt.figure(dpi=300)
    ax = fig.add_subplot(1, 1, 1)
    ax.scatter(wide['YOI'], wide['L/D estimate'], marker='o', label='Widebody')
    ax.scatter(narrow['YOI'], narrow['L/D estimate'], marker='^', label='Narrowbody \& Regional')
    xlabel = 'Aircraft Year of Introduction'
    ylabel ='L/D'
    plt.ylim(10,30)
    future_projections = True
    if future_projections:
        ax.scatter(2025, a350*1.05, color='green', s=30, label='Future Projections')
        ax.axhline(y=limit, color='black', linestyle='-', linewidth=2, label='Theoretical Limit for TW')
        plt.annotate('777X', (2025, a350*1.05,),
                        fontsize=8, xytext=(-10, 5),
                        textcoords='offset points')
        ax.scatter(2030, a340*1.046, color='green', s=30)
        plt.annotate('BLADE', (2030, a340*1.046),
                        fontsize=8, xytext=(-10, 10),
                        textcoords='offset points')
        ax.scatter(2030, a321/factor, color='green')
        plt.annotate('AlbatrossONE', (2030, a321/factor),
                        fontsize=8, xytext=(-10, -13),
                        textcoords='offset points')
        ax.scatter(2035, 27.8, color='green')
        plt.annotate('SB-Wing', (2035, 27.8),
                        fontsize=8, xytext=(-10,5),
                        textcoords='offset points')
        plt.xlim(1955,2050)
    ax.legend(loc='upper left')

    plot.plot_layout(None, xlabel, ylabel, ax)
    if savefig:
        plt.savefig(folder_path+'/aerodynamicsL_over_D_estimation_approach.png', bbox_inches='tight')
    return limit
