import pandas as pd
import math
from test_env.tools import plot
import numpy as np
import matplotlib.pyplot as plt

def calculate(savefig, air_density,flight_vel, g):
    #Dictionary containing engines substitutes, if one engine is not available
    aircraft_data = pd.read_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\Databank.xlsx')
    lift_data = pd.read_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\database_creation\rawdata\aircraftproperties\Aicrraft Range Data Extraction.xlsx', sheet_name='2. Table')
    aircraft_data = aircraft_data.merge(lift_data, on='Name', how='left')

    # factor Beta which accounts for the weight fraction burnt in non cruise phase
    # Martinez et al. used a factor of 0.9 to 0.93 but probably it is better to subtract a certain weight.
    #optimize factor for minimal R-squared between K1 and K2 ?

    beta = lambda x: 0.96 if x == 'Wide' else(0.92 if x =='Narrow' else 0.92)

    aircraft_data['Factor'] = aircraft_data['Type'].apply(beta)
    aircraft_data['Ratio 1']= aircraft_data['Factor']*aircraft_data["MTOW\n(Kg)"]/aircraft_data['MZFW_POINT_1\n(Kg)']
    aircraft_data['Ratio 2']= aircraft_data['Factor']*aircraft_data["MTOW\n(Kg)"]/aircraft_data['MZFW_POINT_2\n(Kg)']
    #aircraft_data['Ratio B']= (aircraft_data['MTOW']-6)/aircraft_data['MZFW_B']
    #aircraft_data['Ratio C']= (aircraft_data['MTOW']-6)/aircraft_data['MZFW_C']

    breguet = aircraft_data

    breguet['Ratio 1']=breguet['Ratio 1'].apply(np.log)
    breguet['Ratio 2']=breguet['Ratio 2'].apply(np.log)

    breguet['K_1']= breguet['RANGE_POINT_1\n(Km)']/breguet['Ratio 1']
    breguet['K_2']= breguet['RANGE_POINT_2\n(Km)']/breguet['Ratio 2']
    breguet['K']=(breguet['K_1']+breguet['K_2'])/2
    #some testing from where this differences might result
    #breguet['delta_K'] = abs(breguet['K_1']-breguet['K_2'])
    #test = breguet[['Name', 'delta_K', 'K_1', 'K_2']]
    #test = test.sort_values(by='delta_K', ascending=False)
    #test = test.drop_duplicates()
    breguet['A'] = breguet['K']*g*0.001*breguet['TSFC Cruise']
    breguet['L/D estimate'] = breguet['A']/flight_vel
    aircraft_data = breguet
    aircraft_data = aircraft_data.drop(columns=['#', 'Aircraft Model Chart',
           'RANGE_POINT_1\n(Km)', 'RANGE_POINT_2\n(Km)', 'MZFW_POINT_1\n(Kg)',
           'MZFW_POINT_2\n(Kg)','Link', 'Factor', 'Ratio 1',
           'Ratio 2', 'K_1', 'K_2', 'K', 'A'])
    aircraft_data['Dmax'] = (g * aircraft_data['MTOW\n(Kg)']) / aircraft_data['L/D estimate']
    aircraft_data['Aspect Ratio'] = aircraft_data['Wingspan,float,metre']**2/aircraft_data['Wing area,float,square-metre']
    aircraft_data['Oswald Efficiency'] = 4.61*(1-0.045*aircraft_data['Aspect Ratio']**0.68)*(math.cos(math.radians(30)))**0.15-3.1 #definition for straight wing
    aircraft_data['c_L'] = (g * aircraft_data['MTOW\n(Kg)']) / (0.5*air_density*flight_vel**2*aircraft_data['Wing area,float,square-metre'])
    aircraft_data['c_D'] = aircraft_data['c_L'] / aircraft_data['L/D estimate']
    aircraft_data['k'] = 1 / (math.pi * aircraft_data['Aspect Ratio'] * aircraft_data['Oswald Efficiency'])
    aircraft_data['c_Di'] = aircraft_data['k']*(aircraft_data['c_L']**2)
    aircraft_data['c_D0'] = aircraft_data['c_D']-aircraft_data['c_Di']
    # second method based on a fixed Oswald Efficiency and CrudFactor
    # not sure if this method works though
    crudfactor = 1 #common for large airlines
    oswald = 0.9 #basic value
    c_D0 = 0.015 #basic value
    aircraft_data['c_D_othermethod'] = crudfactor *(c_D0 +  aircraft_data['c_L']**2/(oswald*math.pi*aircraft_data['Aspect Ratio']))
    aircraft_data['L/D_othermethod'] = aircraft_data['c_L']/aircraft_data['c_D_othermethod']

    aircraft_data.to_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\Databank.xlsx', index=False)

    breguet = aircraft_data.dropna(subset='L/D estimate')
    breguet = breguet.groupby(['Name', 'YOI'], as_index=False).agg({'L/D estimate':'mean'})


    fig = plt.figure(dpi=150)

    # Add a subplot
    ax = fig.add_subplot(1, 1, 1)


    # Plot the dataframes with different symbols
    ax.scatter(breguet['YOI'], breguet['L/D estimate'], marker='o', label='Breguet Range Equation')


    for i, row in breguet.iterrows():
        plt.annotate(row['Name'], (row['YOI'], row['L/D estimate']),fontsize=6, xytext=(-8, 5), textcoords='offset points')
    ax.legend()
    xlabel = 'Year'
    ylabel ='L/D'

    plot.plot_layout(None, xlabel, ylabel, ax)
    if savefig:
        plt.savefig(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\database_creation\graphs\aerodynamicsL_over_D_estimation_approach.png')
