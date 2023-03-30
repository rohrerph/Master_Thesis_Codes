import pandas as pd
import numpy as np
import dict
import matplotlib.pyplot as plt

#load dictionaries
airplanes_dict = dict.AirplaneModels().get_models()
aircraftnames = dict.AircraftNames().get_aircraftnames()
airplanes = airplanes_dict.keys()
airlines = dict.USAirlines().get_airlines()

#Read Data
T2 = pd.read_csv(r"C:\Users\PRohr\Desktop\Masterarbeit\Data\T_SCHEDULE_T2.csv")
AC_types = pd.read_csv(r"C:\Users\PRohr\Desktop\Masterarbeit\Data\L_AIRCRAFT_TYPE (1).csv")
overall = pd.read_excel(r"C:\Users\PRohr\Desktop\Masterarbeit\Data\Data Extraction 2.xlsx", sheet_name='Figure 2')

#Prepare Data from schedule T2
T2 = T2.dropna(subset = ['AVL_SEAT_MILES_320','REV_PAX_MILES_140','AIRCRAFT_FUELS_921'])
T2 = T2.loc[T2['AIRCRAFT_FUELS_921']>0]
T2 = T2.loc[T2['AVL_SEAT_MILES_320']>0]
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
fleet_avg_year= T2.groupby(['YEAR']).agg({'GAL/ASM':'median', 'GAL/RPM':'median'})

AC_type = T2.groupby(['Description']).agg({'GAL/ASM':'median', 'GAL/RPM':'median'})

airplanes_release_year = pd.DataFrame({'Description': list(airplanes), 'YOI': list(airplanes_dict.values())})
airplanes_release_year = pd.merge(AC_type, airplanes_release_year, on='Description')
#change GAL/ASM to MJ/ASK
mj = 142.2 # 142.2 MJ per Gallon of kerosene
km = 1.609344 #miles
airplanes_release_year['MJ/ASK'] = airplanes_release_year['GAL/ASM']*mj/km
fleet_avg_year['MJ/ASK'] = fleet_avg_year['GAL/ASM']*mj/km
n = airplanes_release_year['Description']

#prepare Data from babikian
overall_large_fleet = overall.iloc[:, 9:11]
overall_large_fleet.columns = overall_large_fleet.iloc[0]
overall_large_fleet = overall_large_fleet[1:].dropna()

overall_large = overall.iloc[:, 0:3]
overall_large.columns = overall_large.iloc[0]
overall_large = overall_large[1:].dropna()
overall_large['Label'] = overall_large['Label'].map(aircraftnames)


#which data is in both dataframes?
doubled = pd.merge(overall_large, airplanes_release_year, left_on=['Label','Year'], right_on=['Description', 'YOI'])
doubled['MJ/ASK mixed']=(doubled['EU (MJ/ASK)']+doubled['MJ/ASK'])/2

#Remove values which occur in both Dfs
overall_large = overall_large.loc[~overall_large['Label'].isin(list(doubled['Label']))]
airplanes_release_year = airplanes_release_year.loc[~airplanes_release_year['Description'].isin(list(doubled['Label']))]


fig = plt.figure(dpi=300)

# Add a subplot
ax = fig.add_subplot(1, 1, 1)

ax.scatter(airplanes_release_year['YOI'], airplanes_release_year['MJ/ASK'], marker='^', label='US DOT T2')
ax.scatter(overall_large['Year'], overall_large['EU (MJ/ASK)'], marker='s', label='Large Aircraft Babikian')
ax.scatter(doubled['Year'], doubled['MJ/ASK mixed'], marker='o', label='US DOT T2 & Babikian')
ax.plot(fleet_avg_year.index, fleet_avg_year['MJ/ASK'], label='US DOT T2')
ax.plot(overall_large_fleet['Year'], overall_large_fleet['EU (MJ/ASK)'], label='Babikian Fleet')

for i, row in airplanes_release_year.iterrows():
    plt.annotate(row['Description'], (row['YOI'], row['MJ/ASK']),fontsize=6, xytext=(-10, 5), textcoords='offset points')
# Add a legend to the plot
ax.legend()

#Arrange plot size
plt.ylim(0, 4)
plt.xlim(1955, 2025)
plt.xticks(np.arange(1955, 2024, 10))

# Set the x and y axis labels
ax.set_xlabel('Year')
ax.set_ylabel('EU (MJ/ASK)')

ax.grid(which='major', axis='y', linestyle='-', linewidth = 0.5)
ax.grid(which='minor', axis='y', linestyle='--', linewidth = 0.5)

# Set the plot title
ax.set_title('Overall Efficiency')

plt.savefig('OverallEfficiency_1955_2020.png')

plt.show()