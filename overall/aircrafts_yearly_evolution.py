import pandas as pd
import numpy as np
from tools import dict
import matplotlib.pyplot as plt

#load dictionaries
airplanes_dict = dict.AirplaneModels().get_models()
airplanes = airplanes_dict.keys()
airlines = dict.USAirlines().get_airlines()


T2 = pd.read_csv(r"C:\Users\PRohr\Desktop\Masterarbeit\Data\T_SCHEDULE_T2.csv")
AC_types = pd.read_csv(r"C:\Users\PRohr\Desktop\Masterarbeit\Data\L_AIRCRAFT_TYPE (1).csv")
T2 = T2.dropna(subset = ['AVL_SEAT_MILES_320','REV_PAX_MILES_140','AIRCRAFT_FUELS_921'])
T2 = T2.loc[T2['AIRCRAFT_FUELS_921']>0]
T2 = T2.loc[T2['AVL_SEAT_MILES_320']>0]
T2 = T2.loc[T2['REV_PAX_MILES_140']>0]

#this subgroup 3 contains all "Major Carriers"
T2 = T2.loc[T2['CARRIER_GROUP'] == 3]
#subgroup 1 for aircraft passenger configuration
T2 = T2.loc[T2['AIRCRAFT_CONFIG'] == 1]

#Use the 19 Airlines
T2 = T2.loc[T2['UNIQUE_CARRIER_NAME'].isin(airlines)]
T2 = pd.merge(T2, AC_types, left_on='AIRCRAFT_TYPE', right_on='Code')
T2 = T2.loc[T2['Description'].isin(airplanes)]
T2['GAL/ASM'] = T2['AIRCRAFT_FUELS_921']/T2['AVL_SEAT_MILES_320']
T2['GAL/RPM'] = T2['AIRCRAFT_FUELS_921']/T2['REV_PAX_MILES_140']
T2['Airborne Eff.'] = T2['HOURS_AIRBORNE_650']/T2['ACRFT_HRS_RAMPTORAMP_630']

aircraft_emissions = T2.groupby(['Description','YEAR'], as_index=False).agg({'GAL/ASM':'median', 'GAL/RPM':'median'})
aircraft_emissions = aircraft_emissions.groupby('Description')
def normalize_column(aircraft):
    aircraft['Normalized'] = aircraft['GAL/ASM'] / aircraft['GAL/ASM'].iloc[0]
    return aircraft

aircraft_emissions = aircraft_emissions.apply(normalize_column)

aircraft_dfs = {}
for name in aircraft_emissions['Description'].unique():
    # Get a DataFrame with rows that have the current name
    name_df = aircraft_emissions.loc[aircraft_emissions['Description'] == name]
    # Add the DataFrame to the dictionary with the name as the key
    aircraft_dfs[name] = name_df


# Define the layout of the subplots
nrows = 9
ncols = 5

# Create a figure and subplots using the layout
fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(15, 10), sharex=True)



# Flatten the axes array to simplify indexing
axes = axes.flatten()

# Iterate over the dataframes and plot them on the subplots
for i, (name, df) in enumerate(aircraft_dfs.items()):
    # Plot the dataframe on the current axis
    ax = axes[i]
    #ax.plot(df['YEAR'], df['GAL/ASM'], label='GAL/ASM')
    ax.plot(df['YEAR'], df['Normalized'], label='GAL/ASM')
    #ax.plot(df['YEAR'], df['GAL/RPM'], label='GAL/RPM')
    ax.set_title(name)
    ax.set_xlabel('Year')
    ax.set_ylabel('Value')


fig.tight_layout()
plt.show()


#________PLOT ALL IN ONE PLOT________
fig = plt.figure(dpi=150)

# Add a subplot
ax = fig.add_subplot(1, 1, 1)

for name, df in aircraft_dfs.items():
    # Plot the dataframe on the current axis
    #ax.plot(df['YEAR'], df['GAL/ASM'], label='GAL/ASM')
    ax.plot(df['YEAR'], df['Normalized'], label=name, color='black')
    #ax.plot(df['YEAR'], df['GAL/RPM'], label='GAL/RPM')
    ax.set_title(name)
    ax.set_xlabel('Year')
    ax.set_ylabel('Value')

plt.ylim(0.5, 1.5)
plt.xlim(1990, 2020)

# Set the x and y axis labels
ax.set_xlabel('Year')
ax.set_ylabel('Normalized Fuel Consumption')

# Set the plot title
ax.set_title('Aircraft yearly Fuel consumption compared to YOI')
#ax.legend()

plt.show()