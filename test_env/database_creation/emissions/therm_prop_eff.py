import pandas as pd
import numpy as np
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from not_maintained.tools import plot


def calculate(savefig, flight_speed, folder_path):
    data = pd.read_excel(r'Databank.xlsx')
    data['Overcome Thrust'] = data['Engine Efficiency']*data['Fuel Flow [kg/s]']*43.6*10**6/flight_speed
    data['prop_eff'] = 2 * flight_speed / (data['Overcome Thrust'] / (data['Air Mass Flow [kg/s]'] * data['engineCount']) + 2 * flight_speed)
    data['f'] = data['Fuel Flow [kg/s]']/data['Air Mass Flow [kg/s]']
    data['thermal_eff'] = data['Engine Efficiency']/data['prop_eff']
    data.loc[data['B/P Ratio']<=2, 'thermal_eff'] = np.nan
    data.loc[data['B/P Ratio']<=2, 'prop_eff'] = np.nan
    #\data = data.drop(columns=['Overcome Thrust'])

    data.to_excel(r'Databank.xlsx', index=False)
    #best method probably nu therm via nu prop as other values seem far to small . and there has to be a lot of calibration done, how much thrust is produced by the core and the fan
    data = data.dropna(subset='thermal_eff')
    data = data.loc[data['Type']!='Regional']
    data2 = data.groupby(['Engine Identification', 'YOI'], as_index=False).agg({'thermal_eff':'mean', 'prop_eff':'mean', 'Engine Efficiency':'mean'})

    #colormap for years
    column_data = pd.to_numeric(data2['YOI'])
    # normalize data to range between 0 and 1
    norm = mcolors.Normalize(vmin=column_data.min(), vmax=column_data.max())
    norm_column_data = norm(column_data)
    # create a colormap and map normalized values to colors
    cmap = plt.colormaps.get_cmap('cool')
    colors = cmap(norm_column_data)

    fig = plt.figure(dpi=150)
    ax = fig.add_subplot(1, 1, 1)

    # Plot the dataframes with different symbols
    ax.scatter(data2['prop_eff'], data2['thermal_eff'], marker='o', c=colors)
    #for i, row in data2.iterrows():
        #plt.annotate(row['name_x_y'], (row['prop_eff'], row['thermal_eff']), fontsize=6, xytext=(-8, 5), textcoords='offset points')

    ellipse = Ellipse((0.8, 0.46), 0.08, 0.03, color='b', fill=False, label='Current HBR Engines', angle=135)
    ellipse2 = Ellipse((0.85, 0.48), 0.04, 0.03, color='darkred', fill=False)
    ax.text(0.85, 0.48, 'Future HBR Engines', horizontalalignment='center', verticalalignment='center')
    ellipse3 = Ellipse((0.91, 0.5), 0.03, 0.05, color='r', fill=False)
    ax.text(0.91, 0.5, 'Future Open Rotor Engines', horizontalalignment='center', verticalalignment='center')

    #ax.add_artist(ellipse)
    ax.add_artist(ellipse2)
    ax.add_artist(ellipse3)
    ax.vlines(0.925,0.4,0.65, color='b', label='Theoretical Limit')
    ax.hlines(0.55,0.7,1, color='r', label='Practical Limit NOx', linestyles='--')
    ax.hlines(0.6,0.7,1, color='r', label='Theoretical Limit')

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    plt.colorbar(sm).set_label('Aircraft Year of Introduction')
    ax.legend()
    xlabel = 'Propulsive Efficiency'
    ylabel = 'Thermal Efficiency'
    plt.ylim(0.4, 0.65)
    plt.xlim(0.7, 1)


    plot.plot_layout(None, xlabel, ylabel, ax)
    if savefig:
        plt.savefig(folder_path+'/engine_subefficiency.png')


