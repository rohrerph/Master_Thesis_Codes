import pandas as pd
from test_env.tools import plot
import matplotlib.pyplot as plt
import numpy as np

def calculate(savefig, folder_path):
    # Read SLF data
    slf = pd.read_excel(r"database_creation\rawdata\USDOT\Traffic and Operations 1929-Present_Vollständige D_data.xlsx")
    slf = slf[['Year', 'PLF']]
    slf['PLF'] = slf['PLF'].str.replace(',', '.').astype(float)
    slf = slf[slf['Year'] >= 1959]

    #prepare data and normalize
    data = pd.read_excel(r'Databank.xlsx')
    data = data.sort_values('YOI', ascending=True)
    data = data.merge(slf, left_on='YOI', right_on='Year', how='left')
    data['EI (MJ/RPK)'] = data['EU (MJ/ASK)']/data['PLF']

    # Normalize Data for TSFC, L/D, OEW/Exit Limit and EU using 1959 as a Basis, for OEW normalize regarding heaviest value of each Type
    data['OEW/Exit Limit'] = data.groupby('Type')['OEW/Exit Limit'].transform(lambda x: x / x.max())
    data['OEW/Exit Limit'] = 100 / data['OEW/Exit Limit']
    data = data[['Name','YOI', 'TSFC Cruise','EI (MJ/RPK)', 'OEW/Exit Limit', 'L/D estimate']]
    data = data.dropna()
    oew = data.dropna(subset='OEW/Exit Limit')
    oew['OEW/Exit Limit'] = oew['OEW/Exit Limit'] - 100

    max_tsfc = data.loc[data['YOI']==1959, 'TSFC Cruise'].iloc[0]
    data['TSFC Cruise'] = 100 / (data['TSFC Cruise'] / max_tsfc)
    tsfc = data.dropna(subset='TSFC Cruise')
    tsfc['TSFC Cruise'] = tsfc['TSFC Cruise']-100

    max_eu = data.loc[data['YOI']==1959, 'EI (MJ/RPK)'].iloc[0]
    data['EI (MJ/RPK)'] = 100/ (data['EI (MJ/RPK)'] / max_eu)
    eu = data.dropna(subset='EI (MJ/RPK)')
    eu['EI (MJ/RPK)'] = eu['EI (MJ/RPK)'] - 100

    min_ld = data.loc[data['YOI']==1959, 'L/D estimate'].iloc[0]
    data['L/D estimate'] = 100 / (min_ld / data['L/D estimate'])
    ld = data.dropna(subset='L/D estimate')
    ld['L/D estimate'] = ld['L/D estimate'] - 100

    # Groupby Aircraft by the release Year and take the following years for the IDA
    data = data[['Name','YOI', 'TSFC Cruise','EI (MJ/RPK)', 'OEW/Exit Limit', 'L/D estimate']]
    #data['Multiplied'] = data['TSFC Cruise']*data['OEW/Exit Limit']*data['L/D estimate']
    data = data.dropna()

    years = np.arange(1959, 2022)
    x_all = ld['YOI'].astype(np.int64)
    y_all = ld['L/D estimate'].astype(np.float64)
    z_all = np.polyfit(x_all,  y_all, 4)
    p_all_ld = np.poly1d(z_all)

    x_all = oew['YOI'].astype(np.int64)
    y_all = oew['OEW/Exit Limit'].astype(np.float64)
    z_all = np.polyfit(x_all,  y_all, 4)
    p_all_oew = np.poly1d(z_all)

    x_all = tsfc['YOI'].astype(np.int64)
    y_all = tsfc['TSFC Cruise'].astype(np.float64)
    z_all = np.polyfit(x_all,  y_all, 4)
    p_all_tsfc = np.poly1d(z_all)

    x_all = eu['YOI'].astype(np.int64)
    y_all = eu['EI (MJ/RPK)'].astype(np.float64)
    z_all = np.polyfit(x_all,  y_all, 4)
    p_all_eu = np.poly1d(z_all)

    slf['PLF'] = (100*slf['PLF'] / slf['PLF'].iloc[0]) -100

    # Plot all Data as Scatterpoints and the data for the years above as a line
    fig = plt.figure(dpi=300)
    ax = fig.add_subplot(1, 1, 1)
    x_label = 'Aircraft Year of Introduction'
    y_label = 'Efficiency Increase [%]'

    ax.scatter(tsfc['YOI'], tsfc['TSFC Cruise'],color='black', label='Engine (TSFC)')
    ax.scatter(eu['YOI'], eu['EI (MJ/RPK)'],color='turquoise', label='Overall (MJ/RPK)')
    ax.scatter(oew['YOI'], oew['OEW/Exit Limit'],color='orange', label='Structural (OEW/Exit)')
    ax.scatter(ld['YOI'], ld['L/D estimate'],color='blue', label='Aerodynamic (L/D)')
    ax.scatter(slf['Year'], slf['PLF'], color='green', label='Operational (SLF (1959 normalized))')

    ax.plot(years, p_all_tsfc(years),color='black')
    ax.plot(years, p_all_eu(years),color='turquoise')
    ax.plot(years, p_all_oew(years),color='orange')
    ax.plot(years, p_all_ld(years), color='blue')
    ax.plot(slf['Year'], slf['PLF'], color='green')

    # Add a legend to the plot
    ax.legend()
    plt.xlim(1955, 2025)
    plt.ylim(-30, 400)
    plot.plot_layout(None, x_label, y_label, ax)
    if savefig:
        plt.savefig(folder_path+'/ida_operational_normalized.png')

    # Evaluate the polynomials for the x values
    p_all_tsfc_values = p_all_tsfc(years) + 100
    p_all_oew_values = p_all_oew(years) + 100
    p_all_ld_values = p_all_ld(years) + 100
    p_all_eu_values = p_all_eu(years) + 100
    p_all_slf = slf['PLF'] + 100

    # Create a dictionary with the polynomial values
    data = {
        'YOI': years,
        'TSFC Cruise': p_all_tsfc_values,
        'OEW/Exit Limit': p_all_oew_values,
        'L/D estimate': p_all_ld_values,
        'EU (MJ/ASK)': p_all_eu_values,
        'SLF': p_all_slf
    }

    # Create the DataFrame
    df = pd.DataFrame(data)
    data = df
    # Use LMDI Method

    data['LMDI'] = (data['EU (MJ/ASK)'] - data['EU (MJ/ASK)'].iloc[0]) / (np.log(data['EU (MJ/ASK)']) - np.log(data['EU (MJ/ASK)'].iloc[0]))
    data['Engine_LMDI'] = np.log(data['TSFC Cruise'] / data['TSFC Cruise'].iloc[0])
    data['Aerodyn_LMDI'] = np.log(data['L/D estimate'] / data['L/D estimate'].iloc[0])
    data['Structural_LMDI'] = np.log(data['OEW/Exit Limit'] / data['OEW/Exit Limit'].iloc[0])
    data['SLF_LMDI'] = np.log(data['SLF'] / data['SLF'].iloc[0])
    data['deltaC_Aerodyn_Ops'] = data['LMDI'] * data['Aerodyn_LMDI']
    data['deltaC_Engine_Ops'] = data['LMDI'] * data['Engine_LMDI']
    data['deltaC_Structural_Ops'] = data['LMDI'] * data['Structural_LMDI']
    data['deltaC_SLF_Ops'] = data['LMDI'] * data['SLF_LMDI']
    data['deltaC_Tot_Ops'] = data['EU (MJ/ASK)'] - data['EU (MJ/ASK)'].iloc[0]
    data['deltaC_Res_Ops'] = data['deltaC_Tot_Ops'] - data['deltaC_Aerodyn_Ops'] - data['deltaC_Engine_Ops'] - data['deltaC_Structural_Ops']- data['deltaC_SLF_Ops']

    # Get percentage increase of each efficiency and drop first row which only contains NaN
    data = data[['YOI', 'deltaC_Structural_Ops', 'deltaC_Engine_Ops', 'deltaC_Aerodyn_Ops', 'deltaC_SLF_Ops','deltaC_Res_Ops', 'deltaC_Tot_Ops']]
    data = data.drop(data.index[0])
    dashboard = pd.read_excel(r'Dashboard.xlsx')
    dashboard = dashboard.merge(data, on='YOI')
    dashboard.to_excel(r'Dashboard.xlsx', index=False)
    data = data.set_index('YOI')

    # Set the width of each group and create new indexes just the set the space right
    data = data[['deltaC_Tot_Ops', 'deltaC_SLF_Ops','deltaC_Engine_Ops', 'deltaC_Aerodyn_Ops', 'deltaC_Structural_Ops', 'deltaC_Res_Ops']]

    column_order = ['deltaC_Tot_Ops', 'deltaC_Res_Ops','deltaC_SLF_Ops', 'deltaC_Aerodyn_Ops', 'deltaC_Structural_Ops', 'deltaC_Engine_Ops']

    # Reorder the columns
    data = data[column_order]

    # Create new Labels
    labels = ['Overall (MJ/RPK)', 'Residual' ,'Operational (SLF(1959 Normalized))', 'Aerodynamic (L/D)','Structural (OEW/Exit)','Engine (TSFC)']

    # Create subplots for each column
    fig, ax = plt.subplots(dpi=300)

    # Plot stacked areas for other columns
    data_positive = data.drop('deltaC_Tot_Ops', axis=1).clip(lower=0)
    data_negative = data.drop('deltaC_Tot_Ops', axis=1).clip(upper=0)
    data_negative = data_negative.loc[:, (data_negative != 0).any(axis=0)]
    # Create arrays for stacking the areas
    positive_stack = np.zeros(len(data))
    negative_stack = np.zeros(len(data))

    colors = ['navy','blue', 'royalblue', 'steelblue', 'lightblue']
    for i, column in enumerate(data_positive.columns):
        ax.fill_between(data.index, positive_stack, positive_stack + data_positive.iloc[:, i], color=colors[i],
                        label=labels[i + 1])
        positive_stack += data_positive.iloc[:, i]
    for i, column in enumerate(data_negative.columns):
        ax.fill_between(data.index, negative_stack, negative_stack + data_negative.iloc[:, i], color=colors[i], linewidth=0)
        negative_stack += data_negative.iloc[:, i]

    # Plot overall efficiency as a line
    overall_efficiency = data['deltaC_Tot_Ops']
    ax.plot(data.index, overall_efficiency, color='black', label=labels[0], linewidth= 3)

    xlabel = 'Year'
    ylabel = 'Efficiency Improvements [%]'
    ax.set_xlim(1960, 2020)
    ax.set_ylim(-50, 400)
    ax.legend(loc='upper left')
    plot.plot_layout(None, xlabel, ylabel, ax)

    if savefig:
        plt.savefig(folder_path+'/ida_operational.png')



