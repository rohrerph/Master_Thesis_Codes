import pandas as pd
from not_maintained.tools import dict
import numpy as np
import matplotlib.pyplot as plt

#Dictionary containing engines substitutes, if one engine is not available
substitutes = dict.Substitutes().engine_substitute()
path = r'C:\Users\PRohr\Desktop\Masterarbeit\Data\engine_efficiency.xlsx'
path2 = r'C:\Users\PRohr\Desktop\Masterarbeit\Data\Aircraft Databank v2.xlsx'
engines = pd.read_excel(path)
aircraft_data = pd.read_excel(path2, sheet_name='Lift')
aircraft_data['PL']=aircraft_data['MZFW']-aircraft_data['OEW']
aircraft_data = aircraft_data.dropna(subset='MTOW Range')

#(1-B)*MTOW/MZFW
aircraft_data['MTOW/MZFW'] = (aircraft_data['MTOW'])/aircraft_data['MZFW']
aircraft_data['PL/OEW'] = (aircraft_data['PL'])/aircraft_data['OEW']
breguet = aircraft_data[['MTOW/MZFW', 'MTOW Range', 'Name', 'YOI', 'PL/OEW']]
#MZFW is equal to OEW plus Payload
breguet = breguet.groupby(['Name'], as_index=False).agg({'MTOW/MZFW':'mean',
                                                         'YOI':'mean',
                                                         'MTOW Range':'mean',
                                                         'PL/OEW': 'mean'})

breguet = breguet.merge(engines, left_on=['Name', 'YOI'], right_on=['Name', 'YOI'])
breguet = breguet.dropna(subset='MTOW/MZFW')

g = 9.81
avg_velocity = 240 #m/s which is approximately 0.82 Mach
breguet['MTOW/MZFW log']=breguet['MTOW/MZFW'].apply(np.log)
breguet['K']= breguet['MTOW Range']/breguet['MTOW/MZFW log']
breguet['A'] = breguet['K']*g*0.001*breguet['TSFC Cruise']


breguet['L/D estimate'] = breguet['A']/avg_velocity

fig = plt.figure(dpi=150)

# Add a subplot
ax = fig.add_subplot(1, 1, 1)


# Plot the dataframes with different symbols
ax.scatter(breguet['YOI'], breguet['L/D estimate'], marker='o', label='Aircraft')

for i, row in breguet.iterrows():
    plt.annotate(row['Name'], (row['YOI'], row['L/D estimate']),fontsize=6, xytext=(-8, 5), textcoords='offset points')
ax.legend()
#plt.savefig('L_over_D_estimation_approach.png')

plt.show()