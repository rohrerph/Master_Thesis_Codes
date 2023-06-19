import pandas as pd
from test_env.database_creation.tools import dict, plot
import matplotlib.pyplot as plt
import numpy as np

def calculate(savefig, folder_path):
    airplanes_dict = dict.AirplaneModels().get_models()
    airplanes = airplanes_dict.keys()
    airlines = dict.USAirlines().get_airlines()

    # Air time efficiency in 2022
    AC_types = pd.read_csv(r"C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\database_creation\rawdata\USDOT\L_AIRCRAFT_TYPE (1).csv")
    T100 = pd.read_csv(r"C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\database_creation\rawdata\USDOT\T_T100_SEGMENT_ALL_CARRIER_2022.csv")

    # Use the 19 Airlines
    T100 = T100.loc[T100['UNIQUE_CARRIER_NAME'].isin(airlines)]
    T100 = pd.merge(T100, AC_types, left_on='AIRCRAFT_TYPE', right_on='Code')
    T100 = T100.loc[T100['Description'].isin(airplanes)]
    T100 = T100.loc[T100['AIR_TIME'] > 0]
    T100["DISTANCE"] = T100["DISTANCE"] * 1.62
    T100["PAYLOAD"] = T100["PAYLOAD"] * 0.4535
    T100["PAYLOAD"] = T100["PAYLOAD"] / T100['DEPARTURES_PERFORMED'] / 1000
    T100 = T100.loc[T100.index.repeat(T100['DEPARTURES_PERFORMED'])]
    T100 = T100.reset_index(drop=True)

    # Check for a 777-200 and an A320 and create the payload range diagrams.

    a320 = T100.loc[T100['Description']=='Airbus Industrie A320-100/200']
    b777 = T100.loc[T100['Description']=='Boeing 777-200ER/200LR/233LR']

    #A320 Plot
    a320_boundaries = {
        'Range': [0, 4000, 5200, 6800],
        'Payload': [19.9, 19.9, 15.9, 0]}
    a320_boundaries = pd.DataFrame(a320_boundaries)

    fig, ax = plt.subplots(dpi=300)

    # Calculate the heatmap data
    heatmap, xedges, yedges = np.histogram2d(a320['DISTANCE'], a320['PAYLOAD'], bins=20)
    heatmap[heatmap<5]=0
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

    # Plot the heatmap
    im = ax.imshow(heatmap.T, origin='lower', extent=extent, aspect='auto', cmap='YlGn')
    ax.plot(a320_boundaries['Range'], a320_boundaries['Payload'], label='Limit', color='black')
    # Set labels
    title = 'Payload/Range Diagram'
    xlabel = 'Distance'
    ylabel = 'Payload'
    plot.plot_layout(title, xlabel, ylabel, ax)
    cbar = plt.colorbar(im)
    plt.ylim(0,22)
    plt.xlim(0,6900)
    if savefig:
        plt.savefig(folder_path+ '/a320_payload_range.png')

    # PLOT 777-200 POTENTIALLY BETTER RESULTS

    b777_boundaries = {
        'Range': [0, 14070, 15023, 17687],
        'Payload': [50.352, 50.352, 43.262, 0]}
    b777_boundaries = pd.DataFrame(b777_boundaries)

    fig, ax = plt.subplots(dpi=300)

    # Calculate the heatmap data
    heatmap, xedges, yedges = np.histogram2d(b777['DISTANCE'], b777['PAYLOAD'], bins=20)
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

    # Plot the heatmap
    im = ax.imshow(heatmap.T, origin='lower', extent=extent, aspect='auto', cmap='YlGn')
    ax.plot(b777_boundaries['Range'], b777_boundaries['Payload'], label='Limit', color='black')
    # Set labels
    title = 'Payload/Range Diagram'
    xlabel = 'Distance'
    ylabel = 'Payload'
    plot.plot_layout(title, xlabel, ylabel, ax)
    cbar = plt.colorbar(im)
    if savefig:
        plt.savefig(folder_path+ '/b777_payload_range.png')


    # These heatmaps look way different than the ones from Literature, e.g. Ackert
