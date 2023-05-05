import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from not_maintained.tools import plot, dict
from to_vs_cruise_sfc import cruise_calibration

#Dictionary containing engines substitutes, if one engine is not available

path = r'/overall/data/Databank.xlsx'
aircraft_database = pd.read_excel(path)
substitutes = dict.Substitutes().engine_substitute()
aircraft_database['Engine'] = aircraft_database['Engine'].replace(substitutes)

def get_icao_params(aircraft_database):
    path = r'/not_maintained/engine/output/icao_cruise_emissions.xlsx'
    icao_emissions = pd.read_excel(path)
    aircraft_data = aircraft_database.loc[aircraft_database['Babikian'] == 'No']
    #aircraft_data = aircraft_database.loc[aircraft_database['Check'] == 'Yes']
    ind_engines = aircraft_data['Engine'].drop_duplicates(keep='first').dropna()
    engine_list = list(ind_engines)
    # Create an empty dataframe to store the results
    grouped = pd.DataFrame(columns=['Engine',  'Final Test Date', 'B/P Ratio', 'Pressure Ratio',
           'Rated Thrust (kN)', 'TSFC Cruise'])

    # Loop over the substrings and group the dataframe for each one
    for engine in engine_list:
        # Create a boolean mask for rows that contain the current substring
        mask = icao_emissions['Engine Identification'].str.contains(engine)

        # Sum the 'value_column' for rows that match the mask
        tsfc_cruise = icao_emissions.loc[mask, 'TSFC Cruise'].mean()
        testdate = icao_emissions.loc[mask, 'Final Test Date'].min()
        bpratio = icao_emissions.loc[mask,'B/P Ratio'].mean()
        pressureratio = icao_emissions.loc[mask, 'Pressure Ratio'].mean()
        thrust = icao_emissions.loc[mask, 'Rated Thrust (kN)'].mean()

        # Append the substring and the sum to the results dataframe
        grouped = grouped.append({'Engine': engine,
                                  'TSFC Cruise': tsfc_cruise,
                                  'Final Test Date':testdate,
                                  'B/P Ratio': bpratio,
                                  'Pressure Ratio': pressureratio,
                                  'Rated Thrust (kN)': thrust}, ignore_index=True)

    grouped_nan = grouped[grouped['TSFC Cruise'].isna()]
    grouped_notna = grouped[~grouped['TSFC Cruise'].isna()]

    #5 engines cant be assigned a value from the icao emissions df
    grouped_nan_2 = pd.merge(grouped_nan, aircraft_data[['Engine','Engine TSFC cruise [g/kNs]']])
    print(grouped_nan_2)
    grouped_nan_2['TSFC Cruise']= grouped_nan_2['Engine TSFC cruise [g/kNs]']
    grouped_nan_2 = grouped_nan_2.drop('Engine TSFC cruise [g/kNs]', axis=1)
    grouped_nan_2 = grouped_nan_2.groupby(['Engine'], as_index=False).agg({'TSFC Cruise':'mean'})
    grouped = grouped_notna.append(grouped_nan_2)
    #grouped = grouped.dropna(subset='Final Test Date').reset_index()
    all =grouped
    return all

all = get_icao_params(aircraft_database)
#all.to_excel('output/engine_data.xlsx')
aircraft_database = aircraft_database.merge(all, on='Engine', how='left')
#__________MERGE DATAFRAME ALL BACK TO THE AIRCRAFTS________________

babikian = aircraft_database.loc[aircraft_database['Babikian'] == 'Yes']
babikian = babikian.dropna(subset=['TSFC (mg/Ns)'])
not_babikian = aircraft_database.loc[aircraft_database['Babikian'] == 'No']
rescale = True
if rescale:
    babikian['Engine TSFC take off [g/kNs]'] = (babikian['TSFC (mg/Ns)'] - 8.649)/0.869
    z = cruise_calibration()
    poly = lambda x: z[0] * x + z[1]
    babikian['TSFC Cruise'] = babikian['Engine TSFC take off [g/kNs]'].apply(poly)

#babikian = babikian.loc[babikian['Still in new Metric']=='Yes']
flightspeed = 240 #m/s
heatingvalue = 43.1 #MJ/kg
all = not_babikian.append(babikian)
all['Engine Efficiency'] = flightspeed /(heatingvalue*all['TSFC Cruise'])
all.to_excel('../overall/data/Databank.xlsx', index=False)

# Print the resulting dataframe
#-------------------YEAR vs TSFC CRUISE for AIRCRAFTS-------------------------

fig = plt.figure(dpi=300)
ax = fig.add_subplot(1, 1, 1)

x_all = all['YOI'].astype(np.int64)
y_all = all['TSFC Cruise'].astype(np.float64)
years = pd.Series(range(1955, 2024))
z_all = np.polyfit(x_all,  y_all, 1)
p_all = np.poly1d(z_all)

# Plot the dataframes with different symbols
ax.scatter(babikian['YOI'], babikian['TSFC Cruise'],color='red', marker='s', label='Babikian')
ax.scatter(not_babikian['YOI'], not_babikian['TSFC Cruise'], color='blue',marker='^', label='ICAO ')
#ax.plot(years, p_all(years),color='purple')
#for i, row in babikian.iterrows():
    #plt.annotate(row['Name'], (row['YOI'], row['TSFC Cruise']),fontsize=6, xytext=(-8, 5), textcoords='offset points')
#for i, row in abc.iterrows():
    #plt.annotate(row['Name'], (row['YOI'], row['TSFC Cruise']),fontsize=6, xytext=(-8, 5), textcoords='offset points')
ax.legend()

xlabel = 'Year'
ylabel = 'Cruise TSFC (g/kNs)'
plot.plot_layout(None, xlabel, ylabel, ax)
plt.xlim(1955, 2024)
plt.xticks(np.arange(1955, 2024, 10))
plt.savefig('output/Cruise_TSFC.png')