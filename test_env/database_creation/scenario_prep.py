import pandas as pd
import numpy as np
def calculate():
    mj_to_co2 = 3.16/43.15 #kg CO2 produced per MJ of Jet fuel
    annual_data = pd.read_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\database_creation\rawdata\annualdata.xlsx')
    historic_rpk =pd.read_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\database_creation\rawdata\forecast.xlsx')
    # Create a Tech Freeze Scenario
    future = pd.DataFrame({
        'Year': range(2022, 2051),
        'EU (MJ/ASK)': [annual_data.loc[53, 'EU (MJ/ASK)']] * 29,
        'PLF': [annual_data.loc[53, 'PLF']] * 29,
        'EI (MJ/RPK)': [annual_data.loc[53, 'EI (MJ/RPK)']] * 29
    })
    annual_data = pd.concat([annual_data, future], ignore_index=True)
    annual_data['EI (CO2/RPK)'] = mj_to_co2 * annual_data['EI (MJ/RPK)']
    annual_data['EU (MJ/ASK)'] = mj_to_co2 * annual_data['EI (MJ/RPK)']

    icao_target_start = annual_data.loc[annual_data['Year'] == 2005, 'EI (CO2/RPK)'].values[0]
    icao_percentage_decrease = 0.02
    annual_data['ICAO Target CO2/RPK'] = np.where(annual_data['Year'] >= 2005,
                                          icao_target_start * (1 - icao_percentage_decrease) ** (annual_data['Year'] - 2005),
                                          annual_data['EI (CO2/RPK)'])
    annual_data.loc[annual_data['Year'] < 2005, 'ICAO Target CO2/RPK'] = ''

    # IATA 50% NET EMISSIONS
    rpk_2005 = historic_rpk.loc[historic_rpk['Year'] == 2005, 'Billion RPK'].values[0]
    iata_target_start = annual_data.loc[annual_data['Year'] == 2005, 'EI (CO2/RPK)'].values[0]
    iata_target_start = rpk_2005*iata_target_start
    iata_percentage_decrease = 0.015
    annual_data['IATA Target CO2'] = np.where(annual_data['Year'] >= 2005,
                                          iata_target_start * (1 - iata_percentage_decrease) ** (annual_data['Year'] - 2005),
                                          annual_data['EI (CO2/RPK)'])
    annual_data.loc[annual_data['Year'] < 2005, 'IATA Target CO2'] = ''


    # EUROCONTROL 65% OF ALl EMISSIONS
    rpk_2011 = historic_rpk.loc[historic_rpk['Year'] == 2011, 'Billion RPK'].values[0]
    ec_target_start = annual_data.loc[annual_data['Year'] == 2011, 'EI (CO2/RPK)'].values[0]
    ec_target_start = rpk_2005*ec_target_start
    ec_percentage_decrease = 0.015
    annual_data['EC Target CO2'] = np.where(annual_data['Year'] >= 2011,
                                          ec_target_start * (1 - ec_percentage_decrease) ** (annual_data['Year'] - 2005),
                                          annual_data['EI (CO2/RPK)'])
    annual_data.loc[annual_data['Year'] < 2011, 'EC Target CO2'] = ''
    annual_data = annual_data.merge(historic_rpk, on='Year', how='outer')

    annual_data.to_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\database_creation\annualdata.xlsx', index=False)