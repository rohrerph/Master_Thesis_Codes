import pandas as pd
import dict
import numpy as np
import matplotlib.pyplot as plt

#Dictionary containing engines substitutes, if one engine is not available
substitutes = dict.Substitutes().engine_substitute()
path = r'C:\Users\PRohr\Desktop\Masterarbeit\Python\icao_cruise_emissions.xlsx'
path2 = r'C:\Users\PRohr\Desktop\Masterarbeit\Data\Aircraft Databank v2.xlsx'
icao_emissions = pd.read_excel(path)
aircraft_data = pd.read_excel(path2, sheet_name='New Data Entry')


aircraft_data = aircraft_data.loc[aircraft_data['Check']=='Yes']
aircraft_data['Engine'] = aircraft_data['Engine'].replace(substitutes)
aircraft_data = aircraft_data.drop_duplicates(subset='Engine')
engine_list = list(aircraft_data['Engine'])

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
grouped_nan_2['TSFC Cruise']= grouped_nan_2['Engine TSFC cruise [g/kNs]']
grouped_nan_2 = grouped_nan_2.drop('Engine TSFC cruise [g/kNs]', axis=1)

grouped = grouped_notna.append(grouped_nan_2)
all = grouped
grouped = grouped.dropna(subset='Final Test Date').reset_index()

#__________MERGE DATAFRAME ALL BACK TO THE AIRCRAFTS________________

aircraft_data = pd.read_excel(path2, sheet_name='New Data Entry')
aircraft_data = aircraft_data.loc[aircraft_data['Check']=='Yes']
aircraft_data['Engine'] = aircraft_data['Engine'].replace(substitutes)

abc = aircraft_data.merge(all, on='Engine')
abc = abc.groupby(['Name'], as_index=False).agg({'TSFC Cruise':'mean', 'YOI':'mean'})

babikian = pd.read_excel(path2, sheet_name='Data Table')
babikian = babikian.loc[babikian['Still in new Metric']=='Yes']
babikian = babikian.loc[babikian['Babikian']=='Yes']
babikian = babikian[['Name', 'YOI', 'TSFC (mg/Ns)' ]]
babikian['TSFC Cruise'] = babikian['TSFC (mg/Ns)']
babikian = babikian.drop(['TSFC (mg/Ns)'], axis = 1)

all = babikian.append(abc)
# Print the resulting dataframe
#-------------------YEAR vs TSFC CRUISE-------------------------

y = grouped['TSFC Cruise']
x = grouped['Final Test Date']

fig = plt.figure(dpi=120)
# Add a subplot
ax = fig.add_subplot(1, 1, 1)

ax.scatter(x,y, label='Cruise TSFC')

for i, row in grouped.iterrows():
    plt.annotate(row['Engine'], (row['Final Test Date'], row['TSFC Cruise']),fontsize=6, xytext=(-8, 5), textcoords='offset points')


#ax.plot(years, p(years), label='Average')

ax.legend()

plt.savefig('tsfc_per_engine.png')

plt.show()

# Print the resulting dataframe
#-------------------YEAR vs TSFC CRUISE for AIRCRAFTS-------------------------

fig = plt.figure(dpi=150)

# Add a subplot
ax = fig.add_subplot(1, 1, 1)

x_all = all['YOI'].astype(np.int64)
years = pd.Series(range(1965, 2024))
z_all = np.polyfit(x_all,  all['TSFC Cruise'], 1)
p_all = np.poly1d(z_all)

# Plot the dataframes with different symbols
ax.scatter(babikian['YOI'], babikian['TSFC Cruise'], marker='o', label='Babikian')
ax.scatter(abc['YOI'], abc['TSFC Cruise'], marker='^', label='Added')
ax.plot(years, p_all(years),'-r', label='Added Linear Fit')

for i, row in babikian.iterrows():
    plt.annotate(row['Name'], (row['YOI'], row['TSFC Cruise']),fontsize=6, xytext=(-8, 5), textcoords='offset points')
for i, row in abc.iterrows():
    plt.annotate(row['Name'], (row['YOI'], row['TSFC Cruise']),fontsize=6, xytext=(-8, 5), textcoords='offset points')
ax.legend()
plt.savefig('Cruise_TSFC.png')

plt.show()