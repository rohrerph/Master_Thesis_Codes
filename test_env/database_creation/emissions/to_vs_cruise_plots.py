import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from tools import plot
import matplotlib.colors as mcolors

def calculate(savefig):
    data = pd.read_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\database_creation\rawdata\emissions\all_engines_for_calibration_years.xlsx', skiprows=range(2), header=3, usecols='A,B,C,D,E')
    emissions_df = pd.read_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\Databank.xlsx')
    emissions_df = emissions_df[['Dry weight,integer,kilogram',
                                 'Fan diameter,float,metre',
                                 'Engine Identification',
                                 'TSFC Cruise',
                                 'TSFC T/O',
                                 'B/P Ratio',
                                 'Pressure Ratio',
                                 'Engine Efficiency',
                                 'Name',
                                 'YOI']]
    emissions_df = emissions_df.groupby(['YOI','Name', 'Engine Identification' ], as_index=False).mean()
    yearly_emissions = emissions_df.groupby(['Engine Identification', 'Dry weight,integer,kilogram',
       'Fan diameter,float,metre', 'TSFC Cruise','TSFC T/O', 'B/P Ratio',
       'Pressure Ratio', 'Engine Efficiency'], as_index=False).agg({'YOI':'min'})

    # Get color spectrum for years
    years = yearly_emissions['YOI']
    years2 = data['Release year']

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

    fig = plt.figure(dpi=120)
    # Add a subplot
    ax = fig.add_subplot(1, 1, 1)
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)

    ax.scatter(x, y, c=colors)
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    plt.colorbar(sm).set_label('Date')
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
        plt.savefig(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\database_creation\graphs\weight_vs_diameter.png')


    #plt.savefig('output/icao_takeoff_tsfc.png')

    #-------------------TSFC-------------------------
    fig = plt.figure(dpi=300)
    ax = fig.add_subplot(1, 1, 1)

    y = yearly_emissions['TSFC T/O']

    for value, color in zip(y, colors):
        ax.axvline(x=value, color=color, linewidth=1, ymin=0, ymax=1, alpha=0.5)
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    plt.colorbar(sm).set_label('Date')
    ax.scatter(data['Engine TSFC take off [g/kNs]'], data['Engine TSFC cruise [g/kNs]'], c=colors2, zorder=2)
    xlabel = 'Take-Off TFSC'
    ylabel = 'Cruise TFSC'
    plt.ylim(14, 24)
    plt.xlim(6, 20)
    plot.plot_layout(None, xlabel, ylabel, ax)

    if savefig:
        plt.savefig(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\database_creation\graphs\icao_to_tsfc_vs_years.png')

    # BYPASS RATIO
    fig = plt.figure(dpi=120)

    y = yearly_emissions['Pressure Ratio']
    x = yearly_emissions['B/P Ratio']

    # Add a subplot
    ax = fig.add_subplot(1, 1, 1)

    x_int = x.astype(np.int64)
    years = pd.Series(range(1955, 2024))
    z = np.polyfit(x_int, y, 1)
    p = np.poly1d(z)

    ax.scatter(x_int,y,c=colors, label='B/P Ratio')
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    plt.colorbar(sm).set_label('Date')
    #ax.plot(years, p(years), '-r')
    ax.legend()

    ylabel = 'Pressure Ratio'
    xlabel = 'Bypass Ratio'
    plt.ylim(10, 50)
    plt.xlim(0, 13)
    plot.plot_layout(None, xlabel, ylabel, ax)

    if savefig:
        plt.savefig(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\database_creation\graphs\bypass_vs_pressure_ratio.png')

    # BYPASS RATIO vs Weight
    y = yearly_emissions['Dry weight,integer,kilogram']
    x = yearly_emissions['B/P Ratio']

    fig = plt.figure(dpi=120)

    # Add a subplot
    ax = fig.add_subplot(1, 1, 1)

    x_int = x.astype(np.int64)
    years = pd.Series(range(1955, 2024))
    z = np.polyfit(x_int, y, 1)
    p = np.poly1d(z)

    ax.scatter(x,y,c=colors, marker='o')
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    plt.colorbar(sm).set_label('Date')
    #ax.plot(years, p(years), '-r')

    ylabel = 'Dry Weight [kg]'
    xlabel = 'Bypass Ratio'
    plt.xlim(0, 13)
    plt.ylim(0, 10000)
    plot.plot_layout(None, xlabel, ylabel, ax)

    if savefig:
        plt.savefig(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\database_creation\graphs\bypass_vs_weight.png')
