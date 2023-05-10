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
    data = data.dropna()
    data = data.groupby(['YOI'], as_index=False).agg({'TSFC Cruise':'mean',
       'EU (MJ/ASK)':'mean', 'OEW/Exit Limit':'mean', 'L/D estimate':'mean'})
    years = [1959,1970, 1980, 1990, 2000, 2007, 2018]
    data = data.loc[data['YOI'].isin(years)]

    # Plot all Data as Scatterpoints and the data for the years above as a line
    fig = plt.figure(dpi=300)
    ax = fig.add_subplot(1, 1, 1)
    x_label = 'Year'
    y_label = 'Efficiency'

    ax.scatter(tsfc['YOI'], tsfc['TSFC Cruise'],color='black', label='Engine')
    ax.scatter(eu['YOI'], eu['EU (MJ/ASK)'],color='turquoise', label='Overall')
    ax.scatter(oew['YOI'], oew['OEW/Exit Limit'],color='orange', label='Structural')
    ax.scatter(ld['YOI'], ld['L/D estimate'],color='blue', label='Aerodynamic')
    ax.plot(data['YOI'], data['TSFC Cruise'],color='black', label='Engine')
    ax.plot(data['YOI'], data['EU (MJ/ASK)'],color='turquoise', label='Overall')
    ax.plot(data['YOI'], data['OEW/Exit Limit'],color='orange', label='Structural')
    ax.plot(data['YOI'], data['L/D estimate'],color='blue', label='Aerodynamic')

    # Add a legend to the plot
    ax.legend()
    plt.xlim(1955, 2025)
    plt.ylim(0, 1.2)
    plot.plot_layout(None, x_label, y_label, ax)
    if savefig:
        plt.savefig(folder_path+'/normalized data.png')

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


    # Plotting the grouped bar plots
    fig = plt.figure(dpi=300)
    ax = fig.add_subplot(1, 1, 1)

    # Set the width of each group and create new indexes just the set the space right
    columns = data.columns
    group_width = 1.3
    num_columns = len(data.columns)
    total_width = group_width * num_columns
    new_index = [1970, 1980, 1990, 2000, 2010, 2020]
    data.index = new_index

    # Create new Labels
    labels = ['Structural','Engine', 'Aerodynamic', 'Residual','Overall']

    # Create a Barplot for each Column
    for i, column in enumerate(columns):
        x = data.index + i * group_width
        ax.bar(x, data[column], width=group_width, label=labels[i])

    # Set Labels
    xlabel='YOI'
    ylabel='Efficiency Improvements [%]'
    ax.legend()
    plot.plot_layout(None, xlabel, ylabel, ax)

    #Create new x-Axis Labels
    new_tick_labels = ['1959-1970', '1970-1980', '1981-1990', '1991-2000', '2001-2007', '2008-2018']
    offset = 0.05  # Adjust the offset value as needed
    ax.set_xticks(data.index + (num_columns - 1) * group_width / 2)
    ax.set_xticklabels([f'{label}\n' for label in new_tick_labels], ha='center', va='top', rotation=0)
    for tick in ax.xaxis.get_ticklabels():
        tick.set_y(tick.get_position()[1] - offset)  # Apply the offset to each tick label

    if savefig:
        plt.savefig(folder_path+'/indexdecomposition.png')

