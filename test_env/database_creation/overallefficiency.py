import pandas as pd
import numpy as np
from test_env.tools import dict
from test_env.tools import T2_preprocessing
import matplotlib.pyplot as plt

def calculate(savefig, km, mj, folder_path):

       #load dictionaries
       airplanes_dict = dict.AirplaneModels().get_models()
       aircraftnames = dict.AircraftNames().get_aircraftnames()
       airplanes = airplanes_dict.keys()
       airlines = dict.USAirlines().get_airlines()
       fullnames = dict.fullname().get_aircraftfullnames()

       #Read Data
       T2 = pd.read_csv(r"C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\database_creation\rawdata\USDOT\T_SCHEDULE_T2.csv")
       AC_types = pd.read_csv(r"C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\database_creation\rawdata\USDOT\L_AIRCRAFT_TYPE (1).csv")
       overall = pd.read_excel(r"C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\database_creation\rawdata\aircraftproperties\Data Extraction 2.xlsx", sheet_name='Figure 2')
       aircraft_database = pd.read_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\database_creation\rawdata\aircraftproperties\Aircraft Databank v2.xlsx', sheet_name='New Data Entry')
       historic_slf = pd.read_excel(r"C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\database_creation\rawdata\USDOT\Traffic and Operations 1929-Present_Vollständige D_data.xlsx")

       #Prepare Data from schedule T2
       T2 = T2_preprocessing.preprocessing(T2, AC_types, airlines, airplanes)

       fleet_avg_year= T2.groupby(['YEAR']).agg({'GAL/ASM':'median', 'GAL/RPM':'median'})

       AC_type = T2.groupby(['Description']).agg({'GAL/ASM':'median', 'GAL/RPM':'median', 'Fuel Flow [kg/s]':'mean'})

       airplanes_release_year = pd.DataFrame({'Description': list(airplanes), 'YOI': list(airplanes_dict.values())})
       airplanes_release_year = pd.merge(AC_type, airplanes_release_year, on='Description')
       fuelflow = airplanes_release_year[['Description', 'Fuel Flow [kg/s]']]
       fuelflow.loc[:, 'Description'] = fuelflow['Description'].replace(fullnames)

       airplanes_release_year['MJ/ASK'] = airplanes_release_year['GAL/ASM']*mj/km
       airplanes_release_year['MJ/RPM'] = airplanes_release_year['GAL/RPM']*mj/km

       fleet_avg_year['MJ/ASK'] = fleet_avg_year['GAL/ASM']*mj/km
       fleet_avg_year['MJ/RPK'] = fleet_avg_year['GAL/RPM']*mj/km

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
       doubled['MJ/ASK mixed']=doubled['MJ/ASK']

       #Remove values which occur in both Dfs
       overall_large = overall_large.loc[~overall_large['Label'].isin(list(doubled['Label']))]
       airplanes_release_year = airplanes_release_year.loc[~airplanes_release_year['Description'].isin(list(doubled['Label']))]

       airplanes_release_year = airplanes_release_year.loc[airplanes_release_year['Description'] != 'Embraer-135']
       regionalcarriers = ['Canadair CRJ 900','Canadair RJ-200ER /RJ-440', 'Canadair RJ-700','Embraer 190'
                           'Embraer ERJ-175', 'Embraer-135','Embraer-145']

       regional = airplanes_release_year.loc[airplanes_release_year['Description'].isin(regionalcarriers)]
       normal = airplanes_release_year.loc[~airplanes_release_year['Description'].isin(regionalcarriers)]
       fig = plt.figure(dpi=300)

       # Add a subplot
       ax = fig.add_subplot(1, 1, 1)

       ax.scatter(normal['YOI'], normal['MJ/ASK'], marker='^',color='blue', label='US DOT T2')
       ax.scatter(regional['YOI'], regional['MJ/ASK'], marker='^', color='cyan', label='Regional US DOT T2')
       ax.scatter(overall_large['Year'], overall_large['EU (MJ/ASK)'], marker='s',color='red', label='Babikian')
       ax.scatter(doubled['Year'], doubled['MJ/ASK mixed'], marker='o',color='purple', label='Babikian & US DOT T2')
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
       if savefig:
              plt.savefig(folder_path+ "\ovr_efficiency.png")

       doubled = doubled[['Description','Year', 'MJ/ASK mixed']]
       airplanes_release_year = airplanes_release_year[['Description','YOI','MJ/ASK']]
       doubled = doubled.rename(columns={'Description':'Label', 'Year': 'Year', 'MJ/ASK mixed': 'EU (MJ/ASK)'})
       airplanes_release_year = airplanes_release_year.rename(columns={'Description':'Label', 'YOI': 'Year', 'MJ/ASK':'EU (MJ/ASK)'})

       ovr_eff = pd.concat([doubled, airplanes_release_year, overall_large])
       ovr_eff['Label'] = ovr_eff['Label'].replace(fullnames)

       ovr_eff['Label'] = ovr_eff['Label'].str.strip()
       aircraft_database['Name'] = aircraft_database['Name'].str.strip()

       aircraft_database = aircraft_database.merge(ovr_eff, left_on='Name', right_on='Label', how='left')
       aircraft_database = aircraft_database.merge(fuelflow, left_on='Name', right_on='Description', how='left')
       aircraft_database = aircraft_database.drop(columns=['Label', 'Year', 'Description'])
       aircraft_database = aircraft_database[['Company', 'Name', 'YOI', 'TSFC (mg/Ns)', 'L/Dmax',
              'OEW/MTOW', 'Type', 'Exit Limit', 'OEW','MTOW',
              'Babikian', 'Composites', 'EU (MJ/ASK)', 'Fuel Flow [kg/s]']]
       boeing747 = aircraft_database.loc[aircraft_database['Name']=='B747-400', 'EU (MJ/ASK)'].iloc[0]
       aircraft_database.loc[aircraft_database['Name'] == 'A310-200C/F', 'Fuel Flow [kg/s]'] = np.nan
       aircraft_database.loc[aircraft_database['Name']=='A380', 'EU (MJ/ASK)'] = 0.88*boeing747
       aircraft_database.to_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\Databank.xlsx', index=False)

       #create annual data and calculate Energy Intensity

       fleet_avg_year = fleet_avg_year.reset_index(drop=False)
       fleet_avg_year = fleet_avg_year.loc[:,['YEAR', 'MJ/ASK']].rename(columns={'YEAR':'Year', 'MJ/ASK':'EU (MJ/ASK)'})

       fleet_avg_year = fleet_avg_year.append(overall_large_fleet)
       fleet_avg_year = fleet_avg_year.groupby(['Year'], as_index=False).agg({'EU (MJ/ASK)':'mean'})
       historic_slf['PLF'] = historic_slf['PLF'].str.replace(',', '.').astype(float)
       fleet_avg_year = fleet_avg_year.merge(historic_slf[['Year', 'PLF']], on='Year')
       fleet_avg_year['EI (MJ/RPK)'] = fleet_avg_year['EU (MJ/ASK)']/fleet_avg_year['PLF']
       fleet_avg_year.to_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\database_creation\annualdata.xlsx')