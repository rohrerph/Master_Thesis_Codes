import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
def calculate(limit_tsfc, limit_aero):
    mj_to_co2 = 3.16/43.15 #kg CO2 produced per MJ of Jet fuel
    annual_data = pd.read_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\database_creation\rawdata\annualdata.xlsx')
    historic_rpk =pd.read_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\database_creation\rawdata\forecast.xlsx')
    slf_2019 = annual_data.loc[annual_data['Year'] == 2019, 'PLF'].iloc[0] # get slf from 2019 for baseline scenario, SLF can be changed later.

    # Create a Tech Freeze Scenario
    future = pd.DataFrame({
        'Year': range(2022, 2051),
        'EU (MJ/ASK)': [annual_data.loc[53, 'EU (MJ/ASK)']] * 29,
        'PLF': slf_2019 * 29,
        'EI (MJ/RPK)': [annual_data.loc[53, 'EI (MJ/RPK)']] * 29
    })
    annual_data = pd.concat([annual_data, future], ignore_index=True)
    annual_data['EI (CO2/RPK)'] = mj_to_co2 * annual_data['EI (MJ/RPK)']
    annual_data['EU (MJ/ASK)'] = mj_to_co2 * annual_data['EI (MJ/RPK)']

    # ICAO Target
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

    data = pd.read_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\Databank.xlsx')
    data = data.sort_values('YOI', ascending=True)

    slf = pd.read_excel(r"C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\database_creation\rawdata\USDOT\Traffic and Operations 1929-Present_Vollständige D_data.xlsx")
    slf = slf[['Year', 'PLF']]
    slf['PLF'] = slf['PLF'].str.replace(',', '.').astype(float)

    # Get Baseline Data
    tsfc_baseline = data.loc[data['YOI']==1959, 'TSFC Cruise'].iloc[0]
    ld_baseline = data.loc[data['YOI']==1959, 'L/D estimate'].iloc[0]
    oew_777 = data.loc[data['Name']== '777-300/300ER/333ER', 'OEW/Exit Limit'].iloc[0]
    oew_1959 = data.loc[data['YOI'] == 1959, 'OEW/Exit Limit'].iloc[0]
    #ovr_2021 = historic.loc[historic['YOI'] == 2021, 'EU (MJ/ASK)'].values[0]
    ovr_1959 = data.loc[data['YOI'] == 1959, 'EU (MJ/ASK)'].values[0]
    print(ovr_1959)
    tsfc_2050 = 1 / (limit_tsfc/tsfc_baseline)
    ld_2050 = limit_aero / ld_baseline
    oew_2050 = (oew_777 / oew_1959)*1.2
    ovr_2050_percentage = tsfc_2050 * ld_2050 * oew_2050*100
    ovr_2050 = ovr_1959 / ovr_2050_percentage
    #################################################33
    data = pd.read_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\Databank.xlsx')
    data = data.sort_values('YOI', ascending=True)
    data = data.loc[data['Type']!='Regional']
    data = data[['Name','YOI', 'TSFC Cruise','EU (MJ/ASK)', 'OEW/Exit Limit', 'L/D estimate']]
    data = data.dropna()

    max_eu = data.loc[data['YOI']==1959, 'EU (MJ/ASK)'].iloc[0]
    data['EU (MJ/ASK)'] = 100 / (data['EU (MJ/ASK)'] / max_eu)
    data['EU (MJ/ASK)'] = data['EU (MJ/ASK)'] -100

    x_all = data['YOI'].astype(np.int64)
    y_all = data['EU (MJ/ASK)'].astype(np.float64)
    z_all = np.polyfit(x_all, y_all, 4)
    p_all_eu = np.poly1d(z_all)
    years = np.arange(1959, 2021)
    p_all_eu_values = p_all_eu(years)
    norm = -p_all_eu_values[0]
    p_all_eu_values += norm + 100

    data = {'YOI': years, 'EU (MJ/ASK)': p_all_eu_values}
    new_line = {'YOI': 2050, 'EU (MJ/ASK)': ovr_2050_percentage}
    # Create the DataFrame
    df = pd.DataFrame(data)
    df = df.append(new_line, ignore_index=True)
    print(df)
