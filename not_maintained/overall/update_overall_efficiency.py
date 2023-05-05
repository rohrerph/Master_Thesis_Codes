import pandas as pd
import numpy as np
from not_maintained.tools import T2_preprocessing, dict
import matplotlib.pyplot as plt

#load dictionaries
airplanes_dict = dict.AirplaneModels().get_models()
aircraftnames = dict.AircraftNames().get_aircraftnames()
airplanes = airplanes_dict.keys()
airlines = dict.USAirlines().get_airlines()
fullnames = dict.fullname().get_aircraftfullnames()

#Read Data
T2 = pd.read_csv(r"C:\Users\PRohr\Desktop\Masterarbeit\Data\T_SCHEDULE_T2.csv")
AC_types = pd.read_csv(r"/not_maintained/overall/data/L_AIRCRAFT_TYPE (1).csv")
overall = pd.read_excel(r"C:\Users\PRohr\Desktop\Masterarbeit\Python\overall\data\Data Extraction 2.xlsx", sheet_name='Figure 2')
aircraft_database = pd.read_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\overall\data\Aircraft Databank v2.xlsx', sheet_name='New Data Entry')
historic_slf = pd.read_excel(r"C:\Users\PRohr\Desktop\Masterarbeit\Data\Traffic and Operations 1929-Present_Vollständige D_data.xlsx")

#Prepare Data from schedule T2
T2 = T2_preprocessing.preprocessing(T2, AC_types, airlines, airplanes)

fleet_avg_year= T2.groupby(['YEAR']).agg({'GAL/ASM':'median', 'GAL/RPM':'median'})

AC_type = T2.groupby(['Description']).agg({'GAL/ASM':'median', 'GAL/RPM':'median', 'Fuel Flow [kg/s]':'mean'})


airplanes_release_year = pd.DataFrame({'Description': list(airplanes), 'YOI': list(airplanes_dict.values())})
airplanes_release_year = pd.merge(AC_type, airplanes_release_year, on='Description')
fuelflow = airplanes_release_year[['Description', 'Fuel Flow [kg/s]']]
fuelflow.loc[:, 'Description'] = fuelflow['Description'].replace(fullnames)
#change GAL/ASM to MJ/ASK
mj = 142.2 # 142.2 MJ per Gallon of kerosene
km = 1.609344 #miles
airplanes_release_year['MJ/ASK'] = airplanes_release_year['GAL/ASM']*mj/km
airplanes_release_year['MJ/RPM'] = airplanes_release_year['GAL/RPM']*mj/km
rpm = airplanes_release_year
fleet_avg_year['MJ/ASK'] = fleet_avg_year['GAL/ASM']*mj/km
fleet_avg_year['MJ/RPK'] = fleet_avg_year['GAL/RPM']*mj/km
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

ax.scatter(airplanes_release_year['YOI'], airplanes_release_year['MJ/ASK'], marker='^',color='blue', label='US DOT T2')
ax.scatter(overall_large['Year'], overall_large['EU (MJ/ASK)'], marker='s',color='red', label='Babikian')
ax.scatter(doubled['Year'], doubled['MJ/ASK mixed'], marker='o',color='purple', label='US DOT T2 & Babikian')
ax.plot(fleet_avg_year.index, fleet_avg_year['MJ/ASK'],color='blue', label='US DOT T2 Fleet')
ax.plot(fleet_avg_year.index, fleet_avg_year['MJ/RPK'],color='blue',linestyle='--', label='US DOT T2 Fleet RPK')
ax.plot(overall_large_fleet['Year'], overall_large_fleet['EU (MJ/ASK)'],color='red', label='Babikian Fleet')

#for i, row in airplanes_release_year.iterrows():
    #plt.annotate(row['Description'], (row['YOI'], row['MJ/ASK']),
                 #fontsize=6, xytext=(-10, 5),
                 #textcoords='offset points')

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
ax.grid(which='major', axis='x', linestyle='-', linewidth = 0.5)
# Set the plot title
#ax.set_title('Overall Efficiency')

plt.savefig(r"C:\Users\PRohr\Desktop\Masterarbeit\Python\overall\output\ovr_efficiency.png")

plt.show()

#SAVE RAW DATA
doubled = doubled[['Description','Year', 'MJ/ASK mixed']]
airplanes_release_year = airplanes_release_year[['Description','YOI','MJ/ASK']]

writer = pd.ExcelWriter(r"/not_maintained/overall/output/ovr_efficiency.xlsx")

# Write each DataFrame to a different sheet
doubled.to_excel(writer, sheet_name='USDOTandBABIKIAN', index=False)
airplanes_release_year.to_excel(writer, sheet_name='USDOT', index=False)
overall_large.to_excel(writer, sheet_name='BABIKIAN', index=False)

# Save the Excel file
writer.save()

doubled = doubled.rename(columns={'Description':'Label', 'Year': 'Year', 'MJ/ASK mixed': 'EU (MJ/ASK)'})
airplanes_release_year = airplanes_release_year.rename(columns={'Description':'Label', 'YOI': 'Year', 'MJ/ASK':'EU (MJ/ASK)'})

ovr_eff = pd.concat([doubled, airplanes_release_year, overall_large])
ovr_eff['Label'] = ovr_eff['Label'].replace(fullnames)

ovr_eff['Label'] = ovr_eff['Label'].str.strip()
aircraft_database['Name'] = aircraft_database['Name'].str.strip()

aircraft_database = aircraft_database.merge(ovr_eff, left_on='Name', right_on='Label', how='left')
aircraft_database = aircraft_database.merge(fuelflow, left_on='Name', right_on='Description', how='left')
aircraft_database = aircraft_database.drop(columns=['Label', 'Year', 'Description'])
aircraft_database.to_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\overall\data\Databank.xlsx', index=False)

#create annual data and calculate Energy Intensity

fleet_avg_year = fleet_avg_year.reset_index(drop=False)
fleet_avg_year = fleet_avg_year.loc[:,['YEAR', 'MJ/ASK']].rename(columns={'YEAR':'Year', 'MJ/ASK':'EU (MJ/ASK)'})

fleet_avg_year = fleet_avg_year.append(overall_large_fleet)
fleet_avg_year = fleet_avg_year.groupby(['Year'], as_index=False).agg({'EU (MJ/ASK)':'mean'})
historic_slf['PLF'] = historic_slf['PLF'].str.replace(',', '.').astype(float)
fleet_avg_year = fleet_avg_year.merge(historic_slf[['Year', 'PLF']], on='Year')
fleet_avg_year['EI (MJ/RPK)'] = fleet_avg_year['EU (MJ/ASK)']/fleet_avg_year['PLF']
fleet_avg_year.to_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\overall\output\annualdata.xlsx')