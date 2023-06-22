import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
def calculate(limit_tsfc, limit_aero):
    historic = pd.read_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\Dashboard.xlsx')
    data = pd.read_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\Databank.xlsx')
    data = data.sort_values('YOI', ascending=True)

    slf = pd.read_excel(r"C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\database_creation\rawdata\USDOT\Traffic and Operations 1929-Present_Vollständige D_data.xlsx")
    slf = slf[['Year', 'PLF']]
    slf['PLF'] = slf['PLF'].str.replace(',', '.').astype(float)
    slf = slf[slf['Year'] >= 1959]

    # Get Baseline Data
    tsfc_baseline = data.loc[data['YOI']==1959, 'TSFC Cruise'].iloc[0]
    ld_baseline = data.loc[data['YOI']==1959, 'L/D estimate'].iloc[0]
    oew_baseline = data.loc[data['Name']=='777-300/300ER/333ER', 'OEW/Exit Limit'].iloc[0]
    tsfc_2050 = 1/ (limit_tsfc/tsfc_baseline)
    ld_2050 = limit_aero * ld_baseline
    oew_2050 = oew_baseline*1.2
    ovr_2050 = tsfc_2050 * ld_2050 * oew_2050 # * arbitrary SLF

    #Distribute the residual term equally between the subefficiencies
    res_2020 = historic.loc[historic['YOI'] == 2020, 'deltaC_Res'].values[0]
    res_ops_2020 = historic.loc[historic['YOI'] == 2020, 'deltaC_Res_Ops'].values[0]

    structural_2020 = historic.loc[historic['YOI'] == 2020, 'deltaC_Structural'].values[0]
    structural_2020_ops = historic.loc[historic['YOI'] == 2020, 'deltaC_Structural_Ops'].values[0]
    engine_2020 = historic.loc[historic['YOI'] == 2020, 'deltaC_Engine'].values[0]
    engine_2020_ops = historic.loc[historic['YOI'] == 2020, 'deltaC_Engine_Ops'].values[0]
    aero_2020 = historic.loc[historic['YOI'] == 2020, 'deltaC_Aerodyn'].values[0]
    aero_2020_ops = historic.loc[historic['YOI'] == 2020, 'deltaC_Aerodyn_Ops'].values[0]

    tot_2020_ops = historic.loc[historic['YOI'] == 2020, 'deltaC_Tot_Ops'].values[0]
    slf_2019_ops = historic.loc[historic['YOI'] == 2019, 'deltaC_SLF_Ops'].values[0]
    slf_2020_ops = historic.loc[historic['YOI'] == 2020, 'deltaC_SLF_Ops'].values[0]
    diff = res_ops_2020 - (slf_2019_ops-slf_2020_ops)
    new_row = {
        'YOI': 2021,
        'deltaC_Structural': structural_2020 + res_2020 / 3,
        'deltaC_Engine' : engine_2020 + res_2020 / 3,
        'deltaC_Aerodyn' : aero_2020 + res_2020 / 3,
        'deltaC_Res': 0,
        'deltaC_Tot' : tot_2020,
        'deltaC_Structural_Ops': structural_2020_ops + diff / 3,
        'deltaC_Engine_Ops': engine_2020_ops + diff / 3,
        'deltaC_Aerodyn_Ops':  aero_2020_ops + diff/ 3,
        'deltaC_SLF_Ops' : slf_2019_ops,
        'deltaC_Res_Ops' : 0,
        'deltaC_Tot_Ops':  tot_2020_ops}
    historic = historic.append(new_row, ignore_index=True)

    #####################################################################

    structural_2021 = historic.loc[historic['YOI'] == 2021, 'deltaC_Structural'].values[0]
    structural_2021_ops = historic.loc[historic['YOI'] == 2021, 'deltaC_Structural_Ops'].values[0]
    engine_2021 = historic.loc[historic['YOI'] == 2021, 'deltaC_Engine'].values[0]
    engine_2021_ops = historic.loc[historic['YOI'] == 2021, 'deltaC_Engine_Ops'].values[0]
    aero_2021 = historic.loc[historic['YOI'] == 2021, 'deltaC_Aerodyn'].values[0]
    aero_2021_ops = historic.loc[historic['YOI'] == 2021, 'deltaC_Aerodyn_Ops'].values[0]
    tot_2021 = historic.loc[historic['YOI'] == 2021, 'deltaC_Tot'].values[0]
    tot_2021_ops = historic.loc[historic['YOI'] == 2021, 'deltaC_Tot_Ops'].values[0]
    slf_2021_ops = historic.loc[historic['YOI'] == 2021, 'deltaC_SLF_Ops'].values[0]
    years = range(2022, 2051)

    ########### Build tech freeze scenario
    bau = pd.DataFrame({'YOI': years})
    # Fill values for columns with 2020 value
    columns_to_fill = historic.columns[1:]
    for col in columns_to_fill:
        bau[col] =historic[col].iloc[-1]

    # Concatenate original dataframe and extended dataframe
    bau = pd.concat([historic, bau], ignore_index=True)


    ############### Build Technical Limit Scenario
    limit = pd.DataFrame({'YOI': years})

    columns_to_fill = historic.columns[1:]
    for col in columns_to_fill:
        limit[col] = float('nan')

    #add table for 2050 and then calculate the lmdi and interpolate it for annual values, values on papers, formulate mathematically.

    # Calculate improvements w.r.t. 1959 or 2020, how do I add the correct val for future???
    limit.loc[limit['YOI'] == 2050, ['deltaC_Structural']] = structural_2021*1.2
    limit.loc[limit['YOI'] == 2050, ['deltaC_Engine']] = engine_2021*1.2
    limit.loc[limit['YOI'] == 2050, ['deltaC_Aerodyn']] = aero_2021*1.2
    limit.loc[limit['YOI'] == 2050, ['deltaC_Res']] = 0
    limit.loc[limit['YOI'] == 2050, ['deltaC_Tot']] = 1.2*(aero_2021+ engine_2021+ structural_2021)
    limit.loc[limit['YOI'] == 2050, ['deltaC_Structural_Ops']] = structural_2021_ops*1.2
    limit.loc[limit['YOI'] == 2050, ['deltaC_Engine_Ops']] = engine_2021_ops*1.2
    limit.loc[limit['YOI'] == 2050, ['deltaC_Aerodyn_Ops']] = aero_2021_ops*1.2
    limit.loc[limit['YOI'] == 2050, ['deltaC_Res_Ops']] = 0
    limit.loc[limit['YOI'] == 2050, ['deltaC_SLF_Ops']] = slf_2021_ops
    limit.loc[limit['YOI'] == 2050, ['deltaC_Tot_Ops']] = 1.2*(aero_2021_ops+ engine_2021_ops+ structural_2021_ops)+ slf_2021_ops

    data['Engine_LMDI'] = np.log(10.1/28.2)
    data['Aerodyn_LMDI'] = np.log(data['L/D estimate'] / data['L/D estimate'].iloc[0])
    data['Structural_LMDI'] = np.log(data['OEW/Exit Limit'] / data['OEW/Exit Limit'].iloc[0])
    data['SLF_LMDI'] = np.log(data['SLF'] / data['SLF'].iloc[0])

    limit = pd.concat([historic, limit], ignore_index=True)
    interpolate = limit.columns[limit.columns != 'YOI']

    # Interpolate the selected columns
    limit[interpolate] = limit[interpolate].interpolate()