import pandas as pd
import numpy as np
def calculate():
    ida_data = pd.read_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\Databank.xlsx')
    aircraft_data = pd.read_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\Databank.xlsx')
    annual_data = pd.read_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\database_creation\annualdata.xlsx')

    # Add ICAO Target
    icao_target_start = annual_data.loc[annual_data['Year'] == 2005, 'EI (MJ/RPK)'].values[0]
    icao_percentage_decrease = 0.02
    annual_data['ICAO Target'] = np.where(annual_data['Year'] >= 2005,
                                          icao_target_start * (1 - icao_percentage_decrease) ** (annual_data['Year'] - 2005),
                                          annual_data['EI (MJ/RPK)'])
    annual_data.loc[annual_data['Year'] < 2005, 'ICAO Target'] = ''

    # Add ATAG Target
    atag_target_start = annual_data.loc[annual_data['Year'] == 2009, 'EI (MJ/RPK)'].values[0]
    atag_percentage_decrease = 0.015
    annual_data['ATAG Target'] = np.where(annual_data['Year'] >= 2009,
                                          atag_target_start * (1 - atag_percentage_decrease) ** (annual_data['Year'] - 2009),
                                          annual_data['EI (MJ/RPK)'])
    annual_data.loc[annual_data['Year'] < 2009, 'ATAG Target'] = ''
    annual_data.loc[annual_data['Year'] > 2020, 'ATAG Target'] = ''

    # Add EU Commission, reduce 75% percent of the Fuel Consumption until 2050, this is an annual growth rate of 3.5% annually

    eu_target_start = annual_data.loc[annual_data['Year'] == 2009, 'EI (MJ/RPK)'].values[0]
    eu_percentage_decrease = 0.035
    annual_data['ATAG Target'] = np.where(annual_data['Year'] >= 2009,
                                          eu_target_start * (1 - eu_percentage_decrease) ** (annual_data['Year'] - 2009),
                                          annual_data['EI (MJ/RPK)'])
    annual_data.loc[annual_data['Year'] < 2011, 'ATAG Target'] = ''

    annual_data.to_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\database_creation\annualdata.xlsx', index=False)