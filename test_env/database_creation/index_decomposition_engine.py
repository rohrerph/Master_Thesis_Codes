import pandas as pd
from test_env.tools import plot
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
def calculate(savefig, folder_path):
    # Prepare data and normalize
    data = pd.read_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\Databank.xlsx')
    data = data.sort_values('YOI', ascending=True)
    data = data.loc[data['Type']!='Regional']
    data = data[['Name','YOI','Engine Efficiency', 'prop_eff', 'thermal_eff']]
    data = data.dropna()

    therm = data.loc[data['YOI']==1970, 'thermal_eff'].iloc[0]
    data['thermal_eff'] = (100 / (data['thermal_eff'] / therm))-100
    data['thermal_eff'] = -1 * data['thermal_eff']

    prop = data.loc[data['YOI']==1970, 'prop_eff'].iloc[0]
    data['prop_eff'] = (100 / (data['prop_eff'] / prop))-100
    data['prop_eff'] = -1 * data['prop_eff']

    engine = data.loc[data['YOI']==1970, 'Engine Efficiency'].iloc[0]
    data['Engine Efficiency'] = (100 / (data['Engine Efficiency'] / engine))-100
    data['Engine Efficiency'] = -1 * data['Engine Efficiency']

    years = np.arange(1970, 2021)
    x_all = data['YOI'].astype(np.int64)
    y_all = data['thermal_eff'].astype(np.float64)
    z_all = np.polyfit(x_all,  y_all, 4)
    p_all_thermal = np.poly1d(z_all)

    y_all = data['prop_eff'].astype(np.float64)
    z_all = np.polyfit(x_all,  y_all, 4)
    p_all_prop = np.poly1d(z_all)

    y_all = data['Engine Efficiency'].astype(np.float64)
    z_all = np.polyfit(x_all,  y_all, 4)
    p_all_engine = np.poly1d(z_all)

    # Plot all Data as Scatterpoints and the data for the years above as a line
    fig = plt.figure(dpi=300)
    ax = fig.add_subplot(1, 1, 1)
    x_label = 'Aircraft Year of Introduction'
    y_label = 'Efficiency Increase [%]'

    ax.scatter(data['YOI'], data['Engine Efficiency'],color='black', label='Overall Efficiency')
    ax.scatter(data['YOI'], data['thermal_eff'],color='turquoise', label='Thermal Efficiency')
    ax.scatter(data['YOI'], data['prop_eff'],color='orange', label='Propulsive Efficiency')

    ax.plot(years, p_all_engine(years),color='black')
    ax.plot(years, p_all_thermal(years),color='turquoise')
    ax.plot(years, p_all_prop(years),color='orange')

    # Add a legend to the plot
    ax.legend()
    plt.xlim(1970, 2020)
    plt.ylim(-20, 20)
    plot.plot_layout(None, x_label, y_label, ax)
    if savefig:
        plt.savefig(folder_path+'/ida_engine_normalized.png')

    # Evaluate the polynomials for the x values
    p_all_engine_values = p_all_engine(years) + 100
    p_all_prop_values = p_all_prop(years) + 100
    p_all_thermal_values = p_all_thermal(years) + 100

    # Create a dictionary with the polynomial values
    data = {
        'YOI': years,
        'Overall Efficiency': p_all_engine_values,
        'Propulsive Efficiency': p_all_prop_values,
        'Thermal Efficiency': p_all_thermal_values,
    }
    # Create the DataFrame
    df = pd.DataFrame(data)
    data = df


    # Use LMDI Method

    data['LMDI'] = (data['Overall Efficiency'] - data['Overall Efficiency'].iloc[0]) / (np.log(data['Overall Efficiency']) - np.log(data['Overall Efficiency'].iloc[0]))
    data['Thermal_LMDI'] = np.log(data['Thermal Efficiency'] / data['Thermal Efficiency'].iloc[0])
    data['Prop_LMDI'] = np.log(data['Propulsive Efficiency'] / data['Propulsive Efficiency'].iloc[0])
    data['deltaC_thermal'] = data['LMDI'] * data['Thermal_LMDI']
    data['deltaC_prop'] = data['LMDI'] * data['Prop_LMDI']
    data['deltaC_Tot'] = data['Overall Efficiency'] - data['Overall Efficiency'].iloc[0]
    data['deltaC_Res'] = data['deltaC_Tot'] - data['deltaC_thermal'] - data['deltaC_prop']

    # Get percentage increase of each efficiency and drop first row which only contains NaN
    data = data[['YOI',  'deltaC_Tot', 'deltaC_prop', 'deltaC_thermal', 'deltaC_Res']]
    data = data.drop(0)
    data = data.set_index('YOI')

    columns = data.columns
    group_width = 1.3
    num_columns = len(data.columns)

    # Create new Labels
    labels = ['Overall Efficiency', 'Propulsive Efficiency', 'Thermal Efficiency', 'Residual']

    # Create subplots for each column
    fig, axes = plt.subplots(nrows=1, ncols=num_columns, figsize=(15, 5), dpi=300)

    # Create a Barplot for each Column
    # Iterate over each column
    for i, column in enumerate(columns):
        ax = axes[i]

        # Plot bar plot for each column
        x = data.index + i * group_width
        ax.bar(x, data[column], width=group_width)

        xlabel = 'Year'
        ylabel = 'Efficiency Improvements [%]'
        title = labels[i]
        plot.plot_layout(title, xlabel, ylabel, ax)
        ax.set_xlim(1970,2020)
        ax.set_ylim(-5,20)

    # Adjust spacing between subplots
    plt.tight_layout()
    if savefig:
        plt.savefig(folder_path+'/ida_engine.png')