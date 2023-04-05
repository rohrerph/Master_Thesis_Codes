import pandas as pd
import dict
import numpy as np
import matplotlib.pyplot as plt

#Dictionary containing engines substitutes, if one engine is not available
substitutes = dict.Substitutes().engine_substitute()
path = r'C:\Users\PRohr\Desktop\Masterarbeit\engine_efficiency.xlsx'
path2 = r'C:\Users\PRohr\Desktop\Masterarbeit\Data\Aircraft Databank v2.xlsx'
engines = pd.read_excel(path)
aircraft_data = pd.read_excel(path2, sheet_name='New Data Entry')

aircraft_data['MTOW/MZFW'] = aircraft_data['MTOW']/aircraft_data['MZFW']
breguet = aircraft_data[['MTOW/MZFW', 'Range', 'Name', 'YOI']]
breguet = breguet.groupby(['Name'], as_index=False).agg({'MTOW/MZFW':'mean', 'YOI':'mean', 'Range':'mean'})

breguet = breguet.merge(engines, left_on=['Name', 'YOI'], right_on=['Name', 'YOI'])
breguet = breguet.dropna(subset='MTOW/MZFW')

g = 9.81
avg_velocity = 250 #m/s
breguet['MTOW/MZFW log']=breguet['MTOW/MZFW'].apply(np.log)
breguet['A'] = breguet['Range']*g*0.001*breguet['TSFC Cruise']
breguet['B'] = avg_velocity*breguet['MTOW/MZFW log']

breguet['L/D estimate'] = breguet['A']/breguet['B']

fig = plt.figure(dpi=150)

# Add a subplot
ax = fig.add_subplot(1, 1, 1)


# Plot the dataframes with different symbols
ax.scatter(breguet['YOI'], breguet['L/D estimate'], marker='o', label='Aircraft')

for i, row in breguet.iterrows():
    plt.annotate(row['Name'], (row['YOI'], row['L/D estimate']),fontsize=6, xytext=(-8, 5), textcoords='offset points')
ax.legend()
plt.savefig('L_over_D_estimation_approach.png')

plt.show()