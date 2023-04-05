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

#Fleet averages
fleet_avg= T2.groupby(['YEAR','QUARTER']).agg({'GAL/ASM':'median', 'GAL/RPM':'median'})
fleet_avg.plot(y=['GAL/ASM', 'GAL/RPM'], use_index=True, label=['GAL/ASM', 'GAL/RPM'])
plt.xlabel('Quarter')
plt.ylabel('Values')

fleet_avg_year= T2.groupby(['YEAR']).agg({'GAL/ASM':'median', 'GAL/RPM':'median'})

fleet_avg_year.plot(y=['GAL/ASM', 'GAL/RPM'], use_index=True, label=['GAL/ASM', 'GAL/RPM'])
plt.xlabel('Year')
plt.ylabel('Values')

#monthly and annual, huge spikes in the GAL/ASM when taking the mean value, with median very good results

airborne_efficiency = T2.groupby(['YEAR','QUARTER']).agg({'Airborne Eff.':'median'})
airborne_efficiency.plot(y='Airborne Eff.', use_index=True)
plt.xlabel('Quarter')
plt.ylabel('Airborne efficiency')


airborne_efficiency_year= T2.groupby(['YEAR']).agg({'Airborne Eff.':'median'})
airborne_efficiency_year.plot(y='Airborne Eff.', use_index=True)
plt.xlabel('Year')
plt.ylabel('Airborne efficiency')
plt.show()

#AC_averages
overall = pd.read_excel(r"C:\Users\PRohr\Desktop\Masterarbeit\Data\Data Extraction 2.xlsx", sheet_name='Figure 2')

overall_large_fleet = overall.iloc[:, 9:11]
overall_large_fleet.columns = overall_large_fleet.iloc[0]
overall_large_fleet = overall_large_fleet[1:].dropna()

overall_large = overall.iloc[:, 0:2]
overall_large.columns = overall_large.iloc[0]
overall_large = overall_large[1:].dropna()

AC_type = T2.groupby(['Description']).agg({'GAL/ASM':'median', 'GAL/RPM':'median'})
airplanes_release_year = pd.DataFrame({'Description': list(airplanes), 'YOI': list(airplanes_dict.values())})
airplanes_release_year = pd.merge(AC_type, airplanes_release_year, on='Description')
#change GAL/ASM to MJ/ASK
mj = 142.2 # 142.2 MJ per Gallon of kerosene
km = 1.609344 #miles
airplanes_release_year['MJ/ASK'] = airplanes_release_year['GAL/ASM']*mj/km
fleet_avg_year['MJ/ASK'] = fleet_avg_year['GAL/ASM']*mj/km
n = airplanes_release_year['Description']

fig = plt.figure(dpi=120)

# Add a subplot
ax = fig.add_subplot(1, 1, 1)

ax.scatter(airplanes_release_year['YOI'], airplanes_release_year['MJ/ASK'], marker='^', label='Large Aircraft')
ax.scatter(overall_large['Year'], overall_large['EU (MJ/ASK)'], marker='s', label='Large Aircraft Babikian')
ax.plot(fleet_avg_year.index, fleet_avg_year['MJ/ASK'], label='Large Aircraft Fleet')
ax.plot(overall_large_fleet['Year'], overall_large_fleet['EU (MJ/ASK)'], label='Babikian Fleet')

#for i, txt in enumerate(n):
 #   plt.annotate(txt, (x[i],y[i]))

# Add a legend to the plot
ax.legend()

#Arrange plot size
plt.ylim(0, 4)
plt.xlim(1955, 2020)
plt.xticks(np.arange(1955, 2020, 5))

# Set the x and y axis labels
ax.set_xlabel('Year')
ax.set_ylabel('EU (MJ/ASK)')

# Set the plot title
ax.set_title('Overall Efficiency')

plt.savefig('OverallEfficiency_1955_2020.png')

plt.show()

#per Airline
airline_emissions = T2.groupby(['UNIQUE_CARRIER_NAME','YEAR'], as_index=False).agg({'GAL/ASM':'median', 'GAL/RPM':'median'})
airline_emissions = airline_emissions.groupby('UNIQUE_CARRIER_NAME')
airline_dfs = {}
for name, airline in airline_emissions:
    new_df = pd.DataFrame(airline)
    airline_dfs[name] = new_df
    print(f"DataFrame for {name}:")

# Define the layout of the subplots
nrows = 4
ncols = 5

# Create a figure and subplots using the layout
fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(15, 10), sharex=True)

# Flatten the axes array to simplify indexing
axes = axes.flatten()

# Iterate over the dataframes and plot them on the subplots
for i, (name, df) in enumerate(airline_dfs.items()):
    # Plot the dataframe on the current axis
    ax = axes[i]
    ax.plot(df['YEAR'], df['GAL/ASM'], label='GAL/ASM')
    ax.plot(df['YEAR'], df['GAL/RPM'], label='GAL/RPM')
    ax.set_title(name)
    ax.set_xlabel('Year')
    ax.set_ylabel('Value')

fig.tight_layout()
plt.show()
