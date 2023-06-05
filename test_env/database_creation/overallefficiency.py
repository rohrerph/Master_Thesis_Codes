import pandas as pd
import numpy as np
from test_env.tools import dict
from test_env.tools import T2_preprocessing
from test_env.tools import plot
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
       ax.scatter(overall_large['Year'], overall_large['EU (MJ/ASK)'], marker='s',color='red', label='Lee')
       ax.scatter(doubled['Year'], doubled['MJ/ASK mixed'], marker='o', color='purple', label='Lee & US DOT T2')
       ax.plot(fleet_avg_year.index, fleet_avg_year['MJ/ASK'],color='blue', label='US DOT T2 Fleet')
       ax.plot(fleet_avg_year.index, fleet_avg_year['MJ/RPK'],color='blue',linestyle='--', label='US DOT T2 Fleet RPK')
       ax.plot(overall_large_fleet['Year'], overall_large_fleet['EU (MJ/ASK)'],color='red', label='Lee Fleet')

       historic_legend = ax.legend(loc='upper left', bbox_to_anchor=(1, 1), title="Historic Data", frameon=False)
       historic_legend._legend_box.align = "left"

       #add projections from Lee et al.
       ax.scatter([1997, 2007, 2022], [1.443, 1.238, 0.9578], marker='^', color='black', label='NASA 100 PAX')
       ax.scatter([1997, 2007, 2022], [1.2787, 1.0386, 0.741], marker='*', color='black', label='NASA 150 PAX')
       ax.scatter([1997, 2007, 2022], [1.2267, 0.9867, 0.681], marker='s', color='black', label='NASA 225 PAX')
       ax.scatter([1997, 2007, 2022], [1.1704, 0.9259, 0.637], marker='o', color='black', label='NASA 300 PAX')
       ax.scatter([1997, 2007, 2022], [0.91, 0.76, 0.559], marker='P', color='black', label='NASA 600 PAX')
       ax.scatter(2010, 0.6587 , marker='^', color='grey', label='NRC')
       ax.scatter(2015, 0.5866, marker='o', color='grey', label='Greene')
       ax.scatter([2025, 2025, 2025], [0.55449, 0.6, 0.68], marker='s', color='grey', label='Lee')

       # Projection legend
       projection_handles = ax.get_legend_handles_labels()[0][7:]  # Exclude the first 8 handles (historic data)
       projection_labels = ax.get_legend_handles_labels()[1][7:]  # Exclude the first 8 labels (historic data)
       ax.legend(projection_handles, projection_labels, loc='lower left', bbox_to_anchor=(1, -0.05),
                                     title="Historic Projections", frameon=False)

       ax.add_artist(historic_legend)

       #Arrange plot size
       plt.ylim(0, 4)
       plt.xlim(1955, 2030)
       plt.xticks(np.arange(1955, 2031, 10))

       # Set the x and y axis labels
       xlabel = 'Aircraft Year of Introduction'
       ylabel = 'EU (MJ/ASK)'
       plot.plot_layout(None, xlabel, ylabel, ax)
       if savefig:
              plt.savefig(folder_path+ "\ovr_efficiency.png", bbox_inches='tight')

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
