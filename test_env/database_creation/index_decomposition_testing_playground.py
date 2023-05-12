import pandas as pd
from test_env.tools import plot
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
def calculate(savefig, folder_path):
    # Prepare data and normalize
    data = pd.read_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\Databank.xlsx')
    data = data.sort_values('YOI', ascending=True)

    # Normalize Data for TSFC, L/D, OEW/Exit Limit and EU using 1959 as a Basis, for OEW normalize regarding heaviest value of each Type
    data['OEW/Exit Limit'] = data.groupby('Type')['OEW/Exit Limit'].transform(lambda x: x / x.max())
    data = data[['Name','YOI', 'TSFC Cruise','EU (MJ/ASK)', 'OEW/Exit Limit', 'L/D estimate']]
    data = data.dropna()
    oew = data.dropna(subset='OEW/Exit Limit')

    max_tsfc = data.loc[data['YOI']==1959, 'TSFC Cruise'].iloc[0]
    data['TSFC Cruise'] = data['TSFC Cruise'] / max_tsfc
    tsfc = data.dropna(subset='TSFC Cruise')

    max_eu = data.loc[data['YOI']==1959, 'EU (MJ/ASK)'].iloc[0]
    data['EU (MJ/ASK)'] = data['EU (MJ/ASK)'] / max_eu
    eu = data.dropna(subset='EU (MJ/ASK)')

    min_ld = data.loc[data['YOI']==1959, 'L/D estimate'].iloc[0]
    data['L/D estimate'] = min_ld / data['L/D estimate']
    ld = data.dropna(subset='L/D estimate')

    # Groupby Aircraft by the release Year and take the following years for the IDA
    data = data[['Name','YOI', 'TSFC Cruise','EU (MJ/ASK)', 'OEW/Exit Limit', 'L/D estimate']]
    data['Multiplied'] = data['TSFC Cruise']*data['OEW/Exit Limit']*data['L/D estimate']
    data = data.dropna()

    data2 = data
    years = [1959,1980, 2000, 2018]
    data = data.loc[data['YOI'].isin(years)]

    years = np.arange(1955, 2023)
    x_all = ld['YOI'].astype(np.int64)
    y_all = ld['L/D estimate'].astype(np.float64)
    z_all = np.polyfit(x_all,  y_all, 4)
    p_all_ld = np.poly1d(z_all)
    p_all_ld = p_all_ld / p_all_ld(1959)

    years = np.arange(1955, 2023)
    x_all = oew['YOI'].astype(np.int64)
    y_all = ld['OEW/Exit Limit'].astype(np.float64)
    z_all = np.polyfit(x_all,  y_all, 4)
    p_all_oew = np.poly1d(z_all)
    p_all_oew = p_all_oew / p_all_oew(1959)

    years = np.arange(1955, 2023)
    x_all = tsfc['YOI'].astype(np.int64)
    y_all = tsfc['TSFC Cruise'].astype(np.float64)
    z_all = np.polyfit(x_all,  y_all, 4)
    p_all_tsfc = np.poly1d(z_all)
    p_all_tsfc = p_all_tsfc / p_all_tsfc(1959)

    years = np.arange(1955, 2023)
    x_all = eu['YOI'].astype(np.int64)
    y_all = eu['EU (MJ/ASK)'].astype(np.float64)
    z_all = np.polyfit(x_all,  y_all, 4)
    p_all_eu = np.poly1d(z_all)
    p_all_eu = p_all_eu / p_all_eu(1959)

    # Plot all Data as Scatterpoints and the data for the years above as a line
    fig = plt.figure(dpi=300)
    ax = fig.add_subplot(1, 1, 1)
    x_label = 'Year'
    y_label = 'Efficiency'

    ax.scatter(tsfc['YOI'], tsfc['TSFC Cruise'],color='black', label='Engine')
    ax.scatter(eu['YOI'], eu['EU (MJ/ASK)'],color='turquoise', label='Overall')
    ax.scatter(oew['YOI'], oew['OEW/Exit Limit'],color='orange', label='Structural')
    ax.scatter(ld['YOI'], ld['L/D estimate'],color='blue', label='Aerodynamic')
    ax.scatter(data2['YOI'], data2['Multiplied'],color='purple', label='Multiplied')
    #ax.plot(data['YOI'], data['TSFC Cruise'],color='black', label='Engine')
    #ax.plot(data['YOI'], data['EU (MJ/ASK)'],color='turquoise', label='Overall')
    #ax.plot(data['YOI'], data['OEW/Exit Limit'],color='orange', label='Structural')
    #ax.plot(data['YOI'], data['L/D estimate'],color='blue', label='Aerodynamic')

    ax.plot(years, p_all_tsfc(years),color='black', label='Engine')
    ax.plot(years, p_all_eu(years),color='turquoise', label='Overall')
    ax.plot(years, p_all_oew(years),color='orange', label='Structural')
    ax.plot(years, p_all_ld(years), color='blue', label='Aerodyn')


    # Add a legend to the plot
    ax.legend()
    plt.xlim(1958, 2020)
    plt.ylim(0, 1.2)
    plot.plot_layout(None, x_label, y_label, ax)
    if savefig:
        plt.savefig(folder_path+'/normalizeddata_2.png')

    # Evaluate the polynomials for the x values
    p_all_tsfc_values = p_all_tsfc(years)
    p_all_oew_values = p_all_oew(years)
    p_all_ld_values = p_all_ld(years)
    p_all_eu_values = p_all_eu(years)

    # Create a dictionary with the polynomial values
    data = {
        'YOI': years,
        'TSFC Cruise': p_all_tsfc_values,
        'OEW/Exit Limit': p_all_oew_values,
        'L/D estimate': p_all_ld_values,
        'EU (MJ/ASK)': p_all_eu_values
    }

    # Create the DataFrame
    df = pd.DataFrame(data)


    data = df


    # Use LMDI Method

    data['LMDI'] = (data['EU (MJ/ASK)'].shift(1) - data['EU (MJ/ASK)']) / (np.log(data['EU (MJ/ASK)'].shift(1)) - np.log(data['EU (MJ/ASK)']))
    data['Engine_LMDI'] = np.log(data['TSFC Cruise'].shift(1) / data['TSFC Cruise'])
    data['Aerodyn_LMDI'] = np.log(data['L/D estimate'].shift(1) / data['L/D estimate'])
    data['Structural_LMDI'] = np.log(data['OEW/Exit Limit'].shift(1) / data['OEW/Exit Limit'])
    data['deltaC_Aerodyn'] = data['LMDI'] * data['Aerodyn_LMDI']
    data['deltaC_Engine'] = data['LMDI'] * data['Engine_LMDI']
    data['deltaC_Structural'] = data['LMDI'] * data['Structural_LMDI']
    data['deltaC_Tot'] = data['EU (MJ/ASK)'].shift(1) - data['EU (MJ/ASK)']
    data['deltaC_Res'] = data['deltaC_Tot'] - data['deltaC_Aerodyn'] - data['deltaC_Engine'] - data['deltaC_Structural']

    # Get percentage increase of each efficiency and drop first row which only contains NaN
    data = data[['YOI', 'deltaC_Structural', 'deltaC_Engine', 'deltaC_Aerodyn', 'deltaC_Res', 'deltaC_Tot']]
    data['deltaC_Tot'] = data['deltaC_Tot'] * 100
    data['deltaC_Engine'] = data['deltaC_Engine'] * 100
    data['deltaC_Aerodyn'] = data['deltaC_Aerodyn'] * 100
    data['deltaC_Structural'] = data['deltaC_Structural'] * 100
    data['deltaC_Res'] = data['deltaC_Res'] * 100
    data = data.drop(0)
    data = data.set_index('YOI')
    data.to_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\LMDI.xlsx')


    # Set the width of each group and create new indexes just the set the space right
    data = data[['deltaC_Tot', 'deltaC_Engine', 'deltaC_Aerodyn', 'deltaC_Structural', 'deltaC_Res']]
    columns = data.columns
    group_width = 1.3
    num_columns = len(data.columns)
    total_width = group_width * num_columns

    # Create new Labels
    labels = ['Overall','Engine', 'Aerodyn','Structural', 'Residual' ]

    # Create subplots for each column
    fig, axes = plt.subplots(nrows=1, ncols=num_columns, figsize=(15, 5), dpi=300)

    # Create a Barplot for each Column
    # Iterate over each column
    for i, column in enumerate(columns):
        ax = axes[i]

        # Plot bar plot for each column
        x = data.index + i * group_width
        ax.bar(x, data[column], width=group_width, label=labels[i])

        xlabel = 'YOI'
        ylabel = 'Efficiency Improvements [%]'
        title = column
        plot.plot_layout(title, xlabel, ylabel, ax)
        ax.set_xlim(1959,2021)
        ax.set_ylim(-3,8)

        # Add legend
        ax.legend()

    # Adjust spacing between subplots
    plt.tight_layout()

    if savefig:
        plt.savefig(folder_path+'/indexdecomposition_2.png')