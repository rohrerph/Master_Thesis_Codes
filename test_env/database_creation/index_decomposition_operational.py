import pandas as pd
from test_env.tools import plot
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
def calculate(savefig, folder_path):
    # Read SLF data
    slf = pd.read_excel(r"C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\database_creation\rawdata\USDOT\Traffic and Operations 1929-Present_Vollständige D_data.xlsx")
    slf = slf[['Year', 'PLF']]
    slf['PLF'] = slf['PLF'].str.replace(',', '.').astype(float)
    #prepare data and normalize
    data = pd.read_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\Databank.xlsx')
    data = data.sort_values('YOI', ascending=True)
    data = data.merge(slf, left_on='YOI', right_on='Year', how='left')
    data['EI (MJ/RPK)'] = data['EU (MJ/ASK)']/data['PLF']
    data['OEW/Exit Limit'] = data.groupby('Type')['OEW/Exit Limit'].transform(lambda x: x / x.max())
    max_tsfc = data.loc[data['YOI']==1959, 'TSFC Cruise'].iloc[0]
    data['TSFC Cruise'] = data['TSFC Cruise'] / max_tsfc
    tsfc = data.dropna(subset='TSFC Cruise')
    max_eu = data.loc[data['YOI']==1959, 'EI (MJ/RPK)'].iloc[0]
    data['EI (MJ/RPK)'] = data['EI (MJ/RPK)'] / max_eu
    eu = data.dropna(subset='EI (MJ/RPK)')
    min_ld = data.loc[data['YOI']==1959, 'L/D estimate'].iloc[0]
    data['L/D estimate'] = min_ld / data['L/D estimate']
    ld = data.dropna(subset='L/D estimate')
    min_slf = data.loc[data['YOI']== 1959, 'PLF'].iloc[0]
    data['PLF'] = min_slf / data['PLF']
    oew = data.dropna(subset='OEW/Exit Limit')
    data = data[['Name','YOI', 'TSFC Cruise',
       'EI (MJ/RPK)', 'OEW/Exit Limit', 'L/D estimate', 'PLF']]
    data['Multiplied'] = data['L/D estimate']*data['OEW/Exit Limit']*data['TSFC Cruise']
    data = data.dropna()
    data = data.groupby(['YOI'], as_index=False).agg({'TSFC Cruise':'mean',
       'EI (MJ/RPK)':'mean', 'OEW/Exit Limit':'mean', 'L/D estimate':'mean', 'PLF':'mean'})
    years = [1959,1970, 1980, 1990, 2000, 2007, 2018]
    data = data.loc[data['YOI'].isin(years)]

    fig = plt.figure(dpi=300)

    # Add a subplot
    ax = fig.add_subplot(1, 1, 1)
    x_label = 'Year'
    y_label = 'Efficiency'

    ax.scatter(tsfc['YOI'], tsfc['TSFC Cruise'],color='black', label='Engine')
    ax.scatter(eu['YOI'], eu['EI (MJ/RPK)'],color='turquoise', label='Overall')
    ax.scatter(oew['YOI'], oew['OEW/Exit Limit'],color='orange', label='Structural')
    ax.scatter(ld['YOI'], ld['L/D estimate'],color='blue', label='Aerodynamic')
    ax.plot(data['YOI'], data['TSFC Cruise'],color='black', label='Engine')
    ax.plot(data['YOI'], data['EI (MJ/RPK)'],color='turquoise', label='Overall')
    ax.plot(data['YOI'], data['OEW/Exit Limit'],color='orange', label='Structural')
    ax.plot(data['YOI'], data['L/D estimate'],color='blue', label='Aerodynamic')
    ax.plot(data['YOI'], data['PLF'], color='green', label='Seat Load Factor')

    # Add a legend to the plot
    ax.legend()
    plt.xlim(1955, 2025)
    plt.ylim(0, 1.2)
    plot.plot_layout(None, x_label, y_label, ax)
    plt.show()
    if savefig:
        plt.savefig(folder_path+'/normalized data.png')

    # Select relevant columns for index and factors
    trendline_df=data
    trendline_df['LMDI'] = (trendline_df['EI (MJ/RPK)'].shift(1) - trendline_df['EI (MJ/RPK)']) / ( np.log(trendline_df['EI (MJ/RPK)'].shift(1)) - np.log(trendline_df['EI (MJ/RPK)']))
    trendline_df['Engine_LMDI'] = np.log(trendline_df['TSFC Cruise'].shift(1)/trendline_df['TSFC Cruise'])
    trendline_df['Aerodyn_LMDI'] = np.log(trendline_df['L/D estimate'].shift(1) / trendline_df['L/D estimate'])
    trendline_df['Structural_LMDI'] = np.log(trendline_df['OEW/Exit Limit'].shift(1) / trendline_df['OEW/Exit Limit'])
    trendline_df['Operational_LMDI'] = np.log(trendline_df['PLF'].shift(1) / trendline_df['PLF'])
    trendline_df['deltaC_Aerodyn'] = trendline_df['LMDI']*trendline_df['Aerodyn_LMDI']
    trendline_df['deltaC_Engine'] = trendline_df['LMDI'] * trendline_df['Engine_LMDI']
    trendline_df['deltaC_Structural'] = trendline_df['LMDI'] * trendline_df['Structural_LMDI']
    trendline_df['deltaC_Operational'] = trendline_df['LMDI'] * trendline_df['Operational_LMDI']
    trendline_df['deltaC_Tot'] = trendline_df['EI (MJ/RPK)'].shift(1) - trendline_df['EI (MJ/RPK)']
    trendline_df['deltaC_Res'] = trendline_df['deltaC_Tot']-trendline_df['deltaC_Aerodyn']- trendline_df['deltaC_Engine']-trendline_df['deltaC_Structural']-trendline_df['deltaC_Operational']

    trendline_df = trendline_df[['YOI','deltaC_Structural', 'deltaC_Engine', 'deltaC_Aerodyn', 'deltaC_Operational', 'deltaC_Res','deltaC_Tot']]
    trendline_df['deltaC_Tot'] = trendline_df['deltaC_Tot']*100
    trendline_df['deltaC_Engine'] = trendline_df['deltaC_Engine'] * 100
    trendline_df['deltaC_Aerodyn'] = trendline_df['deltaC_Aerodyn'] * 100
    trendline_df['deltaC_Structural'] = trendline_df['deltaC_Structural'] * 100
    trendline_df['deltaC_Operational'] = trendline_df['deltaC_Operational'] * 100
    trendline_df['deltaC_Res'] = trendline_df['deltaC_Res'] * 100
    trendline_df = trendline_df.drop(0)
    trendline_df = trendline_df.set_index('YOI')
    trendline_df.to_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\LMDI_ops.xlsx')
    columns = trendline_df.columns

    # Plotting the grouped bar plots
    fig = plt.figure(dpi=300)
    ax = fig.add_subplot(1, 1, 1)

    # Set the width of each group
    group_width = 1.3
    num_columns = len(trendline_df.columns)
    total_width = group_width * num_columns
    offset = np.linspace(-total_width / 2, total_width / 2, num_columns)
    new_index = [1970, 1980, 1990, 2000, 2010, 2020]
    trendline_df.index = new_index

    # Iterate over each column and plot the grouped bar plot
    labels = [ 'Structural','Engine', 'Aerodynamic','Operational', 'Residual','Overall']

    for i, column in enumerate(columns):
        x = trendline_df.index + i * group_width
        ax.bar(x, trendline_df[column], width=group_width, label=labels[i])

    xlabel='YOI'
    ylabel='Efficiency Improvements [%]'

    ax.legend()
    plot.plot_layout(None, xlabel, ylabel, ax)
    new_tick_labels = ['1959-1970', '1970-1980', '1981-1990', '1991-2000', '2001-2007', '2008-2018']
    offset = 0.05  # Adjust the offset value as needed
    ax.set_xticks(trendline_df.index + (num_columns - 1) * group_width / 2)
    ax.set_xticklabels([f'{label}\n' for label in new_tick_labels], ha='center', va='top', rotation=0)
    for tick in ax.xaxis.get_ticklabels():
        tick.set_y(tick.get_position()[1] - offset)  # Apply the offset to each tick label
    plt.show()

    if savefig:
        plt.savefig(folder_path+'/indexdecomposition_ops.png')
