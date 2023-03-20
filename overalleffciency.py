import pandas as pd
import numpy as np
import dict
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

#this subgroup 3 contains all "Major Carriers"
T2 = T2.loc[T2['CARRIER_GROUP'] == 3]
#subgroup 1 for aircraft passenger configuration
T2 = T2.loc[T2['AIRCRAFT_CONFIG'] == 1]

T2 = T2.loc[T2['UNIQUE_CARRIER_NAME'].isin(airlines)]
T2 = pd.merge(T2, AC_types, left_on='AIRCRAFT_TYPE', right_on='Code')
T2 = T2.loc[T2['Description'].isin(airplanes)]
T2['GAL/ASM'] = T2['AIRCRAFT_FUELS_921']/T2['AVL_SEAT_MILES_320']
T2['Airborne Eff.'] = T2['HOURS_AIRBORNE_650']/T2['ACRFT_HRS_RAMPTORAMP_630']

#Fleet averages
fleet_avg= T2.groupby(['YEAR','QUARTER']).agg({'GAL/ASM':'median'})
fleet_avg.plot(y='GAL/ASM', use_index=True)
plt.xlabel('Quarter')
plt.ylabel('GAL/ASM')
plt.show()

fleet_avg_year= T2.groupby(['YEAR']).agg({'GAL/ASM':'median'})
fleet_avg_year.plot(y='GAL/ASM', use_index=True)
plt.xlabel('Year')
plt.ylabel('GAL/ASM')
plt.show()
#monthly and annual, huge spikes in the GAL/ASM when taking the mean value, with median very good results

airborne_efficiency = T2.groupby(['YEAR','QUARTER']).agg({'Airborne Eff.':'median'})
airborne_efficiency.plot(y='Airborne Eff.', use_index=True)
plt.xlabel('Quarter')
plt.ylabel('Airborne efficiency')
plt.show()

airborne_efficiency_year= T2.groupby(['YEAR']).agg({'Airborne Eff.':'median'})
airborne_efficiency_year.plot(y='Airborne Eff.', use_index=True)
plt.xlabel('Year')
plt.ylabel('Airborne efficiency')
plt.show()

#AC_averages

AC_type = T2.groupby(['Description']).agg({'GAL/ASM':'median'})
airplanes_release_year = pd.DataFrame({'Description': list(airplanes), 'Release_year': list(airplanes_dict.values())})
airplanes_release_year = pd.merge(AC_type, airplanes_release_year, on='Description')
x = airplanes_release_year['Release_year']
y = airplanes_release_year['GAL/ASM']
n = airplanes_release_year['Description']

plt.scatter(x,y)
plt.xlabel('Year')
plt.ylabel('GAL/ASM')

for i, txt in enumerate(n):
    plt.annotate(txt, (x[i],y[i]))
plt.show()

#AC Type, variations over years ?
airplane = T2.groupby(['Description','YEAR'], as_index=False).agg({'GAL/ASM':'median'})
airplane= airplane.groupby('Description')
dfs = {}
for name, group in airplane:
    new_df = pd.DataFrame(group)
    dfs[name] = new_df
    print(f"DataFrame for {name}:")

# Define the layout of the subplots
nrows = 4
ncols = 5

# Create a figure and subplots using the layout
fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(15, 10),  sharex=True)

# Flatten the axes array to simplify indexing
axes = axes.flatten()

# Iterate over the dataframes and plot them on the subplots
for i, (name, df) in enumerate(dfs.items()):
    # Plot the dataframe on the current axis
    ax = axes[i]
    ax.plot(df['YEAR'], df['GAL/ASM'])
    ax.set_title(name)
    ax.set_xlabel('Year')
    ax.set_ylabel('GAL/ASM')

fig.tight_layout()
plt.show()