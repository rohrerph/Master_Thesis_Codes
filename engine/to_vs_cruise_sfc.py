import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from tools import plot
import matplotlib.colors as mcolors

def cruise_calibration():

    data = pd.read_excel('../overall/data/Databank.xlsx')
    emissions_df = pd.read_excel('data/edb-emissions-databank_v29 (web).xlsx', sheet_name='Gaseous Emissions and Smoke')
    emissions_df['TSFC T/O'] = emissions_df['Fuel Flow T/O (kg/sec)'] / emissions_df['Rated Thrust (kN)'] * 1000
    emissions_df['Final Test Date'] = pd.to_datetime(emissions_df['Final Test Date'])
    emissions_df['Final Test Date'] = emissions_df['Final Test Date'].dt.strftime('%Y')
    yearly_emissions = emissions_df[
        ['Engine Identification', 'Final Test Date', 'Fuel Flow T/O (kg/sec)', 'B/P Ratio', 'Pressure Ratio',
         'Rated Thrust (kN)', 'TSFC T/O']]
    yearly_emissions = yearly_emissions.dropna()

    additional_janes = pd.read_excel('data/additional_engines.xlsx')
    openap = pd.read_excel('data/openap_cruise_tfsc.xlsx')
    openap = openap[['name','cruise_sfc','sealevel_sfc']]
    openap = openap.rename(columns={'cruise_sfc':'Engine TSFC cruise [g/kNs]','sealevel_sfc':'Engine TSFC take off [g/kNs]','name':'Engine'})

    #Locate turbofan database book from Roux
    data = data.append(additional_janes)
    roux = data.loc[(data['Source cruise TSFC']==data['Source TO TSFC']) & (data['Source cruise TSFC']!='Janes Aeroengines')]
    janes = data.loc[(data['Source cruise TSFC']==data['Source TO TSFC']) & (data['Source cruise TSFC']=='Janes Aeroengines')]
    all = data.loc[data['Source cruise TSFC']==data['Source TO TSFC']]
    all = all.append(openap)
    all = all.groupby(['Engine']).agg({'Engine TSFC cruise [g/kNs]':'mean','Engine TSFC take off [g/kNs]':'mean' })
    all.to_excel('data/all_engines_for_calibration.xlsx')
    roux = roux.drop_duplicates(subset='Engine')
    janes = janes.drop_duplicates(subset='Engine')


    #-------------------TAKE OFF vs CRUISE-------------------------
    y_openap = openap['Engine TSFC cruise [g/kNs]']
    x_openap = openap['Engine TSFC take off [g/kNs]']
    y_roux = roux['Engine TSFC cruise [g/kNs]']
    x_roux = roux['Engine TSFC take off [g/kNs]']
    y_janes = janes['Engine TSFC cruise [g/kNs]']
    x_janes = janes['Engine TSFC take off [g/kNs]']
    y_all = all['Engine TSFC cruise [g/kNs]']
    x_all = all['Engine TSFC take off [g/kNs]']
    colors = yearly_emissions['Final Test Date']
    x = yearly_emissions['TSFC T/O']

    fig = plt.figure(dpi=300)
    ax = fig.add_subplot(1, 1, 1)

    z_openap = np.polyfit(x_openap, y_openap, 1)
    p_openap = np.poly1d(z_openap)
    z_roux = np.polyfit(x_roux, y_roux, 1)
    p_roux = np.poly1d(z_roux)
    z_janes = np.polyfit(x_janes, y_janes, 1)
    p_janes = np.poly1d(z_janes)
    z_all = np.polyfit(x_all, y_all, 1)
    p_all = np.poly1d(z_all)
    span = pd.Series(np.arange(8,19,0.2))

    y_mean = np.mean(y_all)
    tss = np.sum((y_all - y_mean)**2)
    y_pred = p_all(x_all)
    rss = np.sum((y_all - y_pred)**2)
    r_squared = 1 - (rss / tss)
    r_squared = r_squared.round(2)

    # extract column data
    column_data = pd.to_numeric(yearly_emissions['Final Test Date'], errors='coerce')
    # normalize data to range between 0 and 1
    norm = mcolors.Normalize(vmin=column_data.min(), vmax=column_data.max())
    norm_column_data = norm(column_data)
    # create a colormap and map normalized values to colors
    cmap = plt.colormaps.get_cmap('PiYG')
    colors = cmap(norm_column_data)

    for value, color in zip(yearly_emissions['TSFC T/O'], colors):
        ax.axvline(x=value, color=color, alpha=0.5, linewidth=1)
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    plt.colorbar(sm).set_label('Final Test Date')

    ax.scatter(x_roux,y_roux, marker='^',color='black',label='Turbofan and Turbojet Engines: Database',zorder=2)
    ax.scatter(x_openap,y_openap, marker='*',color='black', label='Janes Aero-Engines', zorder=2)
    ax.scatter(x_janes,y_janes, marker='o',color='black',label='Nate Meiers Jet Engines', zorder=2)
    #ax.plot(x_roux, p_roux(x_roux),color='blue', label='Turbofan and Turbojet Engines: Database')
    #ax.plot(x_janes, p_janes(x_janes),color='orange', label='Janes Aero-Engines')
    #ax.plot(x_openap, p_openap(x_openap),color='red', label='Nate Meiers Jet Engines')
    ax.plot(span, p_all(span),color='black', label='Combined', linewidth=2)

    equation_text = f'y = {z_all[0]:.2f}x + {z_all[1]:.2f} , R-squared = {r_squared}'
    #can these values be compared to Babikian if a different polynom was used ?
    #Polynom obtained by Lee et al. was 0.869x + 8.65 for comparison
    ax.text(0.35,0.15, equation_text, fontsize=10, color='black', transform=fig.transFigure)
    ax.legend(loc='upper left')

    #Arrange plot size
    plt.ylim(15, 25)
    plt.xlim(6, 20)
    plt.xticks(np.arange(6, 19, 2))

    title = 'TSFC Calibration'
    xlabel = 'Take-Off TSFC [g/kNs]'
    ylabel = 'Cruise TSFC [g/kNs]'
    plot.plot_layout(title, xlabel, ylabel, ax)
    plt.savefig('output/takeoff_vs_cruise_tsfc.png')
    return(z_all)


