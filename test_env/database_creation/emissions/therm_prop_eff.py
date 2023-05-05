import pandas as pd
import numpy as np
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from not_maintained.tools import plot


def calculate(savefig, flight_speed):
    data = pd.read_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\Databank.xlsx')

    #use metric from the book Aircraft Propulsion and Gas Turbine Engines per turbine
    data['Air Mass Core'] = data['Air Mass Flow [kg/s]']/data['B/P Ratio']
    data['Air Mass Fan'] = data['Air Mass Flow [kg/s]'] - data['Air Mass Core']
    data['f'] = data['Fuel Flow [kg/s]']/(data['Air Mass Core']*data['engineCount'])
    # neglect the weight of the fuel mass flow when it is not given.
    data['f'].fillna(0, inplace=True)

    data['Overcome Thrust'] = data['Engine Efficiency']*data['Fuel Flow [kg/s]']*43.6*10**6/flight_speed
    data['Velocity Fan'] = (0.75*data['Overcome Thrust'])/(data['engineCount']*data['Air Mass Fan']) + flight_speed
    data['Velocity Core'] = ((0.25*data['Overcome Thrust']/(data['engineCount']*data['Air Mass Core'])) + flight_speed) / (1+data['f'])

    data['nominator']= 2*flight_speed*(((data['f']+1)*data['Velocity Core']-flight_speed) + data['Bypass ratio,float,None']*(data['Velocity Fan']-flight_speed))
    data['denominator']= ((1+data['f'])*data['Velocity Core']**2-flight_speed**2)+data['Bypass ratio,float,None']*(data['Velocity Fan']**2-flight_speed**2)
    data['prop_eff'] = data['nominator']/data['denominator']
    #propulsive efficiency seems pretty correct in comparison with the data from Kurzke. I think thermal eff. must be calculated regarding the overall efficiency.
    #I think there must be some sort of a rule, as for small BPR this formula seems invalid , maybe a scaling factor for BPR < 4 ?
    data['thermal_eff'] = data['Engine Efficiency']/data['prop_eff']
    abc = data.loc[data['Bypass ratio,float,None']<=2]
    data.loc[data['B/P Ratio']<=2, 'thermal_eff'] = np.nan
    data.loc[data['B/P Ratio']<=2, 'prop_eff'] = np.nan
    data = data.drop(columns=['nominator', 'denominator', 'Velocity Fan', 'Velocity Core', 'Air Mass Core', 'Air Mass Core', 'f', 'Overcome Thrust'])
    #method from Kurzke seems to be less accurate, simply calculating exhaust valocity
    data.to_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\Databank.xlsx', index=False)
    #best method probably nu therm via nu prop as other values seem far to small . and there has to be a lot of calibration done, how much thrust is produced by the core and the fan
    data = data.dropna(subset='thermal_eff')
    data['Company'] = data['Company'].str.strip()
    data = data.loc[data['Company'].isin(['Airbus Industrie','Boeing', 'McDonnell Douglas'])]
    data2 = data.groupby(['Engine Identification', 'Final Test Date'], as_index=False).agg({'thermal_eff':'mean', 'prop_eff':'mean', 'Engine Efficiency':'mean'})

    #colormap for years
    column_data = pd.to_numeric(data2['Final Test Date'])
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

    ellipse = Ellipse((0.8, 0.45), 0.06, 0.06, color='b', fill=False, label='Current HBR Engines')
    ellipse2 = Ellipse((0.85, 0.48), 0.04, 0.03, color='darkred', fill=False)
    ax.text(0.85, 0.48, 'Future HBR Engines', horizontalalignment='center', verticalalignment='center')
    ellipse3 = Ellipse((0.91, 0.5), 0.03, 0.05, color='r', fill=False)
    ax.text(0.91, 0.5, 'Future Open Rotor Engines', horizontalalignment='center', verticalalignment='center')

    ax.add_artist(ellipse)
    ax.add_artist(ellipse2)
    ax.add_artist(ellipse3)
    ax.vlines(0.925,0.4,0.65, color='b', label='Theoretical Limit')
    ax.hlines(0.55,0.7,1, color='r', label='Practical Limit NOx', linestyles='--')
    ax.hlines(0.6,0.7,1, color='r', label='Theoretical Limit')

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    plt.colorbar(sm).set_label('Final Test Date')
    ax.legend()
    xlabel = 'Propulsive Efficiency'
    ylabel = 'Thermal Efficiency'
    plt.ylim(0.4, 0.65)
    plt.xlim(0.7, 1)


    plot.plot_layout(None, xlabel, ylabel, ax)
    if savefig:
        plt.savefig(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\database_creation\graphs\engine_subefficiency.png')


