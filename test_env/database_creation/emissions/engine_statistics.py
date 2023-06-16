import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from test_env.database_creation.tools import plot
import matplotlib.colors as mcolors

def calculate(savefig, folder_path):
    data = pd.read_excel(r'database_creation\rawdata\emissions\all_engines_for_calibration_years.xlsx', skiprows=range(2), header=3, usecols='A,B,C,D,E,F')
    data = data.groupby(['Engine'], as_index=False).agg(
        {'Engine TSFC cruise [g/kNs]': 'mean', 'Engine TSFC take off [g/kNs]': 'mean', 'Release year': 'mean', 'Application Date':'mean'})
    emissions_df = pd.read_excel(r'Databank.xlsx')
    emissions_df = emissions_df[['Dry weight,integer,kilogram',
                                 'Fan diameter,float,metre',
                                 'Engine Identification',
                                 'TSFC Cruise',
                                 'TSFC T/O',
                                 'Overall pressure ratio,float,None',
                                 'B/P Ratio',
                                 'Pressure Ratio',
                                 'Engine Efficiency',
                                 'Name',
                                 'YOI']]
    emissions_df = emissions_df.groupby(['YOI','Name', 'Engine Identification' ], as_index=False).mean()
    yearly_emissions = emissions_df.groupby(['Engine Identification', 'Dry weight,integer,kilogram',
       'Fan diameter,float,metre', 'TSFC Cruise','TSFC T/O', 'B/P Ratio',
       'Pressure Ratio', 'Engine Efficiency', 'Overall pressure ratio,float,None'], as_index=False).agg({'YOI':'min'})

    # Get color spectrum for years
    years = yearly_emissions['YOI']
    years2 = data['Application Date']

    column_data1 = pd.to_numeric(years, errors='coerce')
    column_data2 = pd.to_numeric(years2, errors='coerce')
    norm = mcolors.Normalize(vmin=1959, vmax=2020)
    norm_column_data1 = norm(column_data1)
    norm_column_data2 = norm(column_data2)
    # create a colormap and map normalized values to colors
    cmap = plt.colormaps.get_cmap('cool')
    colors = cmap(norm_column_data1)
    colors2 = cmap(norm_column_data2)

    #-------------------Weight vs Diameter-------------------------
    fig = plt.figure(dpi=300)
    ax = fig.add_subplot(1, 1, 1)
    x = yearly_emissions['Fan diameter,float,metre']
    y = yearly_emissions['Dry weight,integer,kilogram']/1000

    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)

    ax.scatter(x, y, c=colors)
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    plt.colorbar(sm).set_label('Aircraft Release Year')
    xlabel = 'Fan Diameter [m]'
    ylabel = 'Engine Dry Weight [t]'
    plt.ylim(0, 10)
    plt.xlim(0.5, 3.5)
    x = np.linspace(0,3.5, 50)
    y = x**2
    ax.plot(x, y, label='y = x^2')
    ax.legend()
    plot.plot_layout(None, xlabel, ylabel, ax)
    if savefig:
        plt.savefig(folder_path+'\weight_vs_diameter.png')

    #-------------------TSFC-------------------------
    fig = plt.figure(dpi=300)
    ax = fig.add_subplot(1, 1, 1)

    x = data['Engine TSFC take off [g/kNs]']
    y = data['Engine TSFC cruise [g/kNs]']

    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    span = pd.Series(np.arange(7,19,0.2))

    y_mean = np.mean(y)
    tss = np.sum((y - y_mean)**2)
    y_pred = p(x)
    rss = np.sum((y - y_pred)**2)
    r_squared = 1 - (rss / tss)
    r_squared = r_squared.round(2)

    y_emissions = yearly_emissions['TSFC T/O']

    #for value, color in zip(y_emissions, colors):
     #   ax.axvline(x=value, color=color, linewidth=1, ymin=0, ymax=1, alpha=0.5)
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    plt.colorbar(sm).set_label('Engine Year of Certification')
    ax.scatter(x, y, c=colors2, zorder=2)
    ax.plot(span, p(span),color='black', linewidth=2)
    equation_text = f'y = {z[0]:.2f}x + {z[1]:.2f} , R-squared = {r_squared}'
    #Polynom obtained by Lee et al. was 0.869x + 8.65 for comparison
    ax.text(0.30,0.15, equation_text, fontsize=10, color='black', transform=fig.transFigure)
    xlabel = 'Take-Off TSFC'
    ylabel = 'Cruise TSFC'
    plt.ylim(14, 24)
    plt.xlim(6, 20)
    plot.plot_layout(None, xlabel, ylabel, ax)

    if savefig:
        plt.savefig(folder_path+'\icao_to_tsfc_vs_years.png')

    # BYPASS RATIO vs Pressure Ratio
    fig = plt.figure(dpi=300)

    y = yearly_emissions['Overall pressure ratio,float,None']
    x = yearly_emissions['B/P Ratio']

    # Add a subplot
    ax = fig.add_subplot(1, 1, 1)

    ax.scatter(x,y,c=colors)
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    plt.colorbar(sm).set_label('Aircraft Year of Introduction')

    ylabel = 'Pressure Ratio'
    xlabel = 'Bypass Ratio'
    plt.ylim(10, 55)
    plt.xlim(0, 13)
    plot.plot_layout(None, xlabel, ylabel, ax)

    if savefig:
        plt.savefig(folder_path+'/bypass_vs_pressure_ratio.png')

    # BYPASS RATIO vs Weight
    fig = plt.figure(dpi=300)
    ax = fig.add_subplot(1, 1, 1)

    y = yearly_emissions['Fan diameter,float,metre']
    x = yearly_emissions['B/P Ratio']

    ax.scatter(x, y, c=colors, marker='o')
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    plt.colorbar(sm).set_label('Aircraft Year of Introduction')

    ylabel = 'Fan Diameter [m]'
    xlabel = 'Bypass Ratio'
    plt.xlim(0, 13)
    plt.ylim(0, 4)
    plot.plot_layout(None, xlabel, ylabel, ax)

    if savefig:
        plt.savefig(folder_path+'/bypass_vs_dia.png')
