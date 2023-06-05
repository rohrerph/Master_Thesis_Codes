import pandas as pd
from test_env.tools import dict
from test_env.tools import plot
import geopandas as gpd
from shapely.geometry import Point
from shapely.geometry import LineString
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

def calculate(vel, savefig, folder_path):
    airplanes_dict = dict.AirplaneModels().get_models()
    airplanes = airplanes_dict.keys()
    airlines = dict.USAirlines().get_airlines()

    # Air time efficiency in 2022
    AC_types = pd.read_csv(
        r"database_creation/rawdata/USDOT/L_AIRCRAFT_TYPE (1).csv")
    T100 = pd.read_csv(r"database_creation/rawdata/USDOT/T_T100_SEGMENT_ALL_CARRIER_2022.csv")
    airport_coordinates = pd.read_csv(r"database_creation/rawdata/USDOT/airports.csv")
    airport_coordinates = airport_coordinates.loc[airport_coordinates['type']=='large_airport']

    # Use the 19 Airlines
    T100 = T100.loc[T100['UNIQUE_CARRIER_NAME'].isin(airlines)]
    T100 = pd.merge(T100, AC_types, left_on='AIRCRAFT_TYPE', right_on='Code')
    T100 = T100.loc[T100['Description'].isin(airplanes)]
    T100 = T100.loc[T100['AIR_TIME'] > 0]
    T100["DISTANCE"] = T100["DISTANCE"]*1.62
    T100["MIN TIME"] = T100["DISTANCE"]/vel
    T100["JOURNEY"] = T100["ORIGIN"]+"-"+T100['DEST']

    T100['JOURNEY'] = T100['JOURNEY'].apply(lambda x: '-'.join(sorted(x.split('-'))))


    T100 = T100.groupby('JOURNEY', as_index=False).agg({'DEPARTURES_PERFORMED': 'sum','AIR_TIME':'sum', 'RAMP_TO_RAMP':'sum', 'MIN TIME':'mean', 'DISTANCE':'mean'})
    T100['AIR_TIME'] = T100['AIR_TIME']/T100['DEPARTURES_PERFORMED']
    T100['RAMP_TO_RAMP'] = T100['RAMP_TO_RAMP']/T100['DEPARTURES_PERFORMED']
    T100['AIR_TIME_EFF'] = T100['MIN TIME']/T100['AIR_TIME']

    # -------------------Weight vs Diameter-------------------------
    fig = plt.figure(dpi=300)
    ax = fig.add_subplot(1, 1, 1)

    x = T100['DISTANCE']
    y = T100['AIR_TIME_EFF']

    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    ax.scatter(x, y, marker='o',label='Actual Flights')


    xlabel = 'Distance [km]'
    ylabel = 'Airtime Efficiency'

    ax.legend()
    plot.plot_layout(None, xlabel, ylabel, ax)
    if savefig:
        plt.savefig(folder_path + '/airtimeefficiency.png')


    # Create Map for A Airport, here JFK
    T100 = T100.loc[T100['JOURNEY'].str.contains('JFK')]
    gdf = gpd.GeoDataFrame({'JOURNEY': T100['JOURNEY']})

    # Create a column with start and end airport coordinates
    gdf['start'] = gdf['JOURNEY'].apply(lambda x: x.split('-')[0])
    gdf['end'] = gdf['JOURNEY'].apply(lambda x: x.split('-')[1])


    # Merge the journey DataFrame with the airport coordinates DataFrame
    gdf = gdf.merge(airport_coordinates, left_on='start', right_on='iata_code', how='left')
    journey_df = gdf.merge(airport_coordinates, left_on='end', right_on='iata_code', how='left', suffixes=['_start', '_end'])
    # Drop unnecessary columns
    journey_df['start_geom'] = journey_df.apply(lambda row: Point(row['longitude_deg_start'], row['latitude_deg_start']), axis=1)
    journey_df['end_geom'] = journey_df.apply(lambda row: Point(row['longitude_deg_end'], row['latitude_deg_end']), axis=1)

    journey_df = journey_df.dropna(subset=['latitude_deg_start', 'longitude_deg_start', 'latitude_deg_end', 'longitude_deg_end'])


    journey_df = journey_df[['JOURNEY','start_geom', 'end_geom']]
    journey_df = journey_df[~journey_df['JOURNEY'].str.contains('\d')]

    journey_df = journey_df.merge(T100, on='JOURNEY')

    journey_df['line'] = journey_df.apply(lambda row: LineString([row['start_geom'], row['end_geom']]), axis=1)
    journey_df= journey_df[['JOURNEY', 'AIR_TIME_EFF', 'line']]

    gdf = gpd.GeoDataFrame(journey_df, geometry=journey_df['line'])

    column_data = pd.to_numeric(gdf['AIR_TIME_EFF'], errors='coerce')
    norm = mcolors.Normalize(vmin=0.5, vmax=1)
    norm_column_data = norm(column_data)
    cmap = plt.colormaps.get_cmap('cool')
    colors = cmap(norm_column_data)

    # Load a world map shapefile or GeoDataFrame
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    # Create a new figure and axis
    fig = plt.figure(dpi=300)
    ax = fig.add_subplot(1, 1, 1)

    # Plot the world map
    world.plot(ax=ax, color='lightgray')

    # Plot the line strings
    gdf.plot(ax=ax, color=colors, linewidth=0.5)

    # Set the axis labels
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    plt.colorbar(sm).set_label('Airtime Efficiency')

    ax.set_xlim(-130, -40)
    ax.set_ylim(10, 60)

    if savefig:
        plt.savefig(folder_path + '/airtimeefficiency_map.png')
