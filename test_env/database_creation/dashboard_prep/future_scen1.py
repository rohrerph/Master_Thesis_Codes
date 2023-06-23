import pandas as pd
import numpy as np
def calculate(limit_tsfc, limit_aero):
    mj_to_co2 = 3.16 / 43.15  # kg CO2 produced per MJ of Jet fuel
    slf = pd.read_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\database_creation\rawdata\annualdata.xlsx')
    historic_rpk = pd.read_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\database_creation\rawdata\forecast.xlsx')
    annual_data = pd.read_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\database_creation\rawdata\annualdata.xlsx')
    slf_2019 = slf.loc[slf['Year'] == 2019, 'PLF'].iloc[0]

    # Create a Tech Freeze Scenario
    future = pd.DataFrame({
        'Year': range(2022, 2051),
        'EU (MJ/ASK)': [annual_data.loc[53, 'EU (MJ/ASK)']] * 29,
        'PLF': [slf_2019] * 29  ,
        'EI (MJ/RPK)': [annual_data.loc[53, 'EI (MJ/RPK)']] * 29
    })
    techfreeze = pd.concat([annual_data, future], ignore_index=True)
    techfreeze['EI (CO2/RPK)'] = mj_to_co2 * techfreeze['EI (MJ/RPK)']
    techfreeze['EU (CO2/ASK)'] = mj_to_co2 * techfreeze['EU (MJ/ASK)']
    techfreeze.to_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\database_creation\dashboard_prep\techfreeze.xlsx')


    # Tech Limit Scenario
    data = pd.read_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\Databank.xlsx')
    data = data.sort_values('YOI', ascending=True)

    # Get Baseline Data
    tsfc_baseline = data.loc[data['YOI'] == 1959, 'TSFC Cruise'].iloc[0]
    ld_baseline = data.loc[data['YOI'] == 1959, 'L/D estimate'].iloc[0]
    oew_777 = data.loc[data['Name'] == '777-300/300ER/333ER', 'OEW/Exit Limit'].iloc[0]
    oew_1959 = data.loc[data['YOI'] == 1959, 'OEW/Exit Limit'].iloc[0]
    ovr_1959 = data.loc[data['YOI'] == 1959, 'EU (MJ/ASK)'].values[0]
    tsfc_2050 = 1 / (limit_tsfc / tsfc_baseline)
    ld_2050 = limit_aero / ld_baseline
    oew_2050 = (oew_777 / oew_1959) * 1.2
    ovr_2050_percentage = tsfc_2050 * ld_2050 * oew_2050
    ovr_2050_eu = ovr_1959 / ovr_2050_percentage
    ovr_2050_ei = ovr_2050_eu/slf_2019
    future = pd.DataFrame({
        'Year': [2022, 2050],
        'EU (MJ/ASK)': [annual_data.loc[53, 'EU (MJ/ASK)'], ovr_2050_eu],
        'PLF': [slf_2019] * 2  ,
        'EI (MJ/RPK)': [annual_data.loc[53, 'EI (MJ/RPK)'], ovr_2050_ei]})

    years = np.arange(2022, 2051)
    years = pd.DataFrame(years, columns=['Year'])
    future = future.merge(years, on='Year', how='outer')
    future = future.sort_values(by=['Year'])
    future = future.interpolate()

    techlimit = pd.concat([annual_data, future], ignore_index=True)
    techlimit['EI (CO2/RPK)'] = mj_to_co2 * techlimit['EI (MJ/RPK)']
    techlimit['EU (CO2/ASK)'] = mj_to_co2 * techlimit['EU (MJ/ASK)']
    techlimit.to_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\database_creation\dashboard_prep\techlimit.xlsx')

    # Create further Scenarios
    # also the scenarios from iata could be defined.

    ###############################     TARGER SCENARIOS
    # ICAO Target 60% Reduction per CO2/RPK
    target = annual_data
    target = target.merge(years, how='outer')
    target['EI (CO2/RPK)'] = mj_to_co2 * target['EI (MJ/RPK)']

    icao_target_start = target.loc[target['Year'] == 2005, 'EI (CO2/RPK)'].values[0]
    icao_percentage_decrease = 0.02
    target['ICAO Target CO2/RPK'] = np.where(target['Year'] >= 2005,
                                          icao_target_start * (1 - icao_percentage_decrease) ** (target['Year'] - 2005),
                                          target['EI (CO2/RPK)'])
    target.loc[target['Year'] < 2005, 'ICAO Target CO2/RPK'] = ''

    # IATA 50% NET EMISSIONS
    rpk_2005 = historic_rpk.loc[historic_rpk['Year'] == 2005, 'Billion RPK'].values[0]
    iata_target_start = target.loc[target['Year'] == 2005, 'EI (CO2/RPK)'].values[0]
    iata_target_start = rpk_2005*iata_target_start
    iata_percentage_decrease = 0.015
    target['IATA Target CO2'] = np.where(target['Year'] >= 2005,
                                          iata_target_start * (1 - iata_percentage_decrease) ** (target['Year'] - 2005),
                                          target['EI (CO2/RPK)'])
    target.loc[target['Year'] < 2005, 'IATA Target CO2'] = ''

    # EUROCONTROL 65% OF ALl EMISSIONS
    rpk_2011 = historic_rpk.loc[historic_rpk['Year'] == 2011, 'Billion RPK'].values[0]
    ec_target_start = target.loc[target['Year'] == 2011, 'EI (CO2/RPK)'].values[0]
    ec_target_start = rpk_2005*ec_target_start
    ec_percentage_decrease = 0.015
    target['EC Target CO2'] = np.where(target['Year'] >= 2011,
                                          ec_target_start * (1 - ec_percentage_decrease) ** (target['Year'] - 2005),
                                          target['EI (CO2/RPK)'])
    target.loc[target['Year'] < 2011, 'EC Target CO2'] = ''
    target = target.merge(historic_rpk, on='Year', how='outer')
    target = target[['Year', 'ICAO Target CO2/RPK', 'IATA Target CO2', 'EC Target CO2', 'Billion RPK']]
    target.to_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\database_creation\dashboard_prep\target.xlsx')
