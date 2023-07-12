import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from test_env.database_creation.tools import plot
def calculate(limit_tsfc, limit_aero, savefig, folder_path):
    mj_to_co2 = 3.16 / 43.15  # kg CO2 produced per MJ of Jet fuel
    slf = pd.read_excel(r'database_creation\rawdata\annualdata.xlsx')
    historic_rpk = pd.read_excel(r'database_creation\rawdata\forecast.xlsx')
    annual_data = pd.read_excel(r'database_creation\rawdata\annualdata.xlsx')
    data = pd.read_excel(r'Databank.xlsx')
    data = data.sort_values('YOI', ascending=True)
    slf_2019 = slf.loc[slf['Year'] == 2019, 'PLF'].iloc[0]

    years = np.arange(2021, 2051)
    years = pd.DataFrame(years, columns=['Year'])

    # Create a Tech Freeze Scenario, assume in 2040 all aircraft are swapped by the A321neo
    a321neo = data.loc[data['Name'] == 'A321-200n', 'EU (MJ/ASK)'].values[0]
    future = pd.DataFrame({
        'Year': [2021, 2040],
        'EU (MJ/ASK)': [annual_data.loc[53, 'EU (MJ/ASK)'], a321neo],
        'PLF': [slf_2019] * 2,
        'EI (MJ/RPK)': [annual_data.loc[53, 'EI (MJ/RPK)'], a321neo/slf_2019]})
    future = future.merge(years, on='Year', how='outer')
    future = future.sort_values(by=['Year'])
    future = future.interpolate()
    future = future[future['Year']!=2021]

    techfreeze = pd.concat([annual_data, future], ignore_index=True)
    techfreeze['EI (CO2/RPK)'] = mj_to_co2 * techfreeze['EI (MJ/RPK)']
    techfreeze['EU (CO2/ASK)'] = mj_to_co2 * techfreeze['EU (MJ/ASK)']
    techfreeze.to_excel(r'dashboard_creation\techfreeze.xlsx')

    # Tech Limit Scenario, assumption to reach tech limit in 2050
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
        'Year': [2021, 2050],
        'EU (MJ/ASK)': [annual_data.loc[53, 'EU (MJ/ASK)'], ovr_2050_eu],
        'PLF': [slf_2019] * 2  ,
        'EI (MJ/RPK)': [annual_data.loc[53, 'EI (MJ/RPK)'], ovr_2050_ei]})

    future = future.merge(years, on='Year', how='outer')
    future = future.sort_values(by=['Year'])
    future = future.interpolate()
    future = future[future['Year']!=2021]

    techlimit = pd.concat([annual_data, future], ignore_index=True)
    techlimit['EI (CO2/RPK)'] = mj_to_co2 * techlimit['EI (MJ/RPK)']
    techlimit['EU (CO2/ASK)'] = mj_to_co2 * techlimit['EU (MJ/ASK)']
    techlimit.to_excel(r'dashboard_creation\techlimit.xlsx')

    # NASA HWB301-GTF AIRCRAFT, assume techfreeze scenario until 2040 then from 2040 until 2050 complete change to BWB

    b777 = data.loc[data['Name'] == 'B777', 'EU (MJ/ASK)'].values[0]
    future = pd.DataFrame({
        'Year': [2021, 2040, 2050],
        'EU (MJ/ASK)': [annual_data.loc[53, 'EU (MJ/ASK)'], a321neo, 0.53*b777],
        'PLF': [slf_2019] * 3,
        'EI (MJ/RPK)': [annual_data.loc[53, 'EI (MJ/RPK)'], a321neo/slf_2019, 0.53*b777/slf_2019]})
    future = future.merge(years, on='Year', how='outer')
    future = future.sort_values(by=['Year'])
    future = future.interpolate()
    future = future[future['Year']!=2021]

    bwb = pd.concat([annual_data, future], ignore_index=True)
    bwb['EI (CO2/RPK)'] = mj_to_co2 * bwb['EI (MJ/RPK)']
    bwb['EU (CO2/ASK)'] = mj_to_co2 * bwb['EU (MJ/ASK)']
    bwb.to_excel(r'dashboard_creation\bwb.xlsx')

    # NASA ADVANCED TUBE WING CONCEPT ALSO BASED ON THE 777-200
    future = pd.DataFrame({
        'Year': [2021, 2040, 2050],
        'EU (MJ/ASK)': [annual_data.loc[53, 'EU (MJ/ASK)'], a321neo, 0.547*b777],
        'PLF': [slf_2019] * 3,
        'EI (MJ/RPK)': [annual_data.loc[53, 'EI (MJ/RPK)'], a321neo/slf_2019, 0.547*b777/slf_2019]})
    future = future.merge(years, on='Year', how='outer')
    future = future.sort_values(by=['Year'])
    future = future.interpolate()
    future = future[future['Year']!=2021]

    advancedtw = pd.concat([annual_data, future], ignore_index=True)
    advancedtw['EI (CO2/RPK)'] = mj_to_co2 * advancedtw['EI (MJ/RPK)']
    advancedtw['EU (CO2/ASK)'] = mj_to_co2 * advancedtw['EU (MJ/ASK)']
    advancedtw.to_excel(r'dashboard_creation\advancedtw.xlsx')

    # MIT DOUBLE BUBBLE D8 AIRCRAFT BASED ON THE 737-800
    start = annual_data.loc[53, 'EU (MJ/ASK)']
    a321neo_2035 = a321neo + (start - a321neo)*(5/20)
    b737_8 = data.loc[data['Name'] == '737-800', 'EU (MJ/ASK)'].values[0]
    future = pd.DataFrame({
        'Year': [2021, 2035, 2045, 2050],
        'EU (MJ/ASK)': [annual_data.loc[53, 'EU (MJ/ASK)'], a321neo_2035, 0.341*b737_8,  0.341*b737_8],
        'PLF': [slf_2019] * 4,
        'EI (MJ/RPK)': [annual_data.loc[53, 'EI (MJ/RPK)'], a321neo_2035/slf_2019, 0.341*b737_8/slf_2019,  0.341*b737_8/slf_2019]})
    future = future.merge(years, on='Year', how='outer')
    future = future.sort_values(by=['Year'])
    future = future.interpolate()
    future = future[future['Year']!=2021]

    doublebubble = pd.concat([annual_data, future], ignore_index=True)
    doublebubble['EI (CO2/RPK)'] = mj_to_co2 * doublebubble['EI (MJ/RPK)']
    doublebubble['EU (CO2/ASK)'] = mj_to_co2 * doublebubble['EU (MJ/ASK)']
    doublebubble.to_excel(r'dashboard_creation\doublebubble.xlsx')

    # Truss Braced Wings
    future = pd.DataFrame({
        'Year': [2021, 2035, 2045, 2050],
        'EU (MJ/ASK)': [annual_data.loc[53, 'EU (MJ/ASK)'], a321neo_2035, 0.7*a321neo,  0.7*a321neo],
        'PLF': [slf_2019] * 4,
        'EI (MJ/RPK)': [annual_data.loc[53, 'EI (MJ/RPK)'], a321neo_2035/slf_2019, 0.7*a321neo/slf_2019,  0.7*a321neo/slf_2019]})
    future = future.merge(years, on='Year', how='outer')
    future = future.sort_values(by=['Year'])
    future = future.interpolate()
    future = future[future['Year']!=2021]

    ttwb = pd.concat([annual_data, future], ignore_index=True)
    ttwb['EI (CO2/RPK)'] = mj_to_co2 * ttwb['EI (MJ/RPK)']
    ttwb['EU (CO2/ASK)'] = mj_to_co2 * ttwb['EU (MJ/ASK)']
    ttwb.to_excel(r'dashboard_creation\ttwb.xlsx')


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
    ec_target_start = rpk_2011*ec_target_start
    ec_percentage_decrease = 0.015
    target['EC Target CO2'] = np.where(target['Year'] >= 2011,
                                          ec_target_start * (1 - ec_percentage_decrease) ** (target['Year'] - 2011),
                                          target['EI (CO2/RPK)'])
    target.loc[target['Year'] < 2011, 'EC Target CO2'] = ''
    target = target.merge(historic_rpk, on='Year', how='outer')
    target = target[['Year', 'ICAO Target CO2/RPK', 'IATA Target CO2', 'EC Target CO2', 'Billion RPK']]
    target.to_excel(r'dashboard_creation\target.xlsx')

    fig = plt.figure(dpi=300)

    # Add a subplot
    ax = fig.add_subplot(1, 1, 1)

    ax.plot(techfreeze['Year'],techfreeze['EU (MJ/ASK)'],color='red', label= 'Tech Freeze')
    ax.plot(techlimit['Year'], techlimit['EU (MJ/ASK)'], color='blue', label='Tech Limit')
    ax.plot(advancedtw['Year'], advancedtw['EU (MJ/ASK)'], color='purple', label='Advanced TW')
    ax.plot(bwb['Year'], bwb['EU (MJ/ASK)'], color='green', label='Blended Wing Body')
    ax.plot(doublebubble['Year'], doublebubble['EU (MJ/ASK)'], color='grey', label='Double Bubble D8')
    ax.plot(ttwb['Year'], ttwb['EU (MJ/ASK)'], color='pink', label='Strut-Braced Wing')
    ax.legend()
    ylabel = 'Energy Usage (MJ/ASK)'
    xlabel = 'Year'
    plot.plot_layout(None, xlabel, ylabel, ax)
    plt.xlim(2020, 2050)
    plt.ylim(0, 1.5)

    if savefig:
        plt.savefig(folder_path+'/futurefleeteff.png')

    ### Compare annual value with the single aircraft values
    annual_data = pd.read_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\database_creation\rawdata\annualdata.xlsx')
    annual_data = annual_data[['Year', 'EU (MJ/ASK)']]
    annual_data = annual_data.rename(columns={'Year': 'YOI'})
    data = pd.read_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\Databank.xlsx')
    data = data.loc[data['Type']!='Regional']
    data = data[['YOI', 'EU (MJ/ASK)']]
    data = data.rename(columns={'EU (MJ/ASK)': 'EU Aircraft'})
    data = data.merge(annual_data, on='YOI', how='outer')
    data = data.sort_values('YOI')
    data = data.fillna(0)
    # Lets still see if this could work...