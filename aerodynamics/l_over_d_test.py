import pandas as pd
from tools import dict
from tools import plot
import numpy as np
import matplotlib.pyplot as plt

#Dictionary containing engines substitutes, if one engine is not available
substitutes = dict.Substitutes().engine_substitute()
path = r'C:\Users\PRohr\Desktop\Masterarbeit\Data\engine_efficiency.xlsx'
path2 = r'C:\Users\PRohr\Desktop\Masterarbeit\Data\Aircraft Databank v2.xlsx'
engines = pd.read_excel(path)
aircraft_data = pd.read_excel(path2, sheet_name='Lift')
aircraft_data = aircraft_data.dropna(subset='MTOW')

# factor Beta which accounts for the weight fraction burnt in non cruise phase
# Martinez et al. used a factor of 0.9 to 0.93 but probably it is better to subtract a certain weight.
aircraft_data['Ratio B']= 0.935*aircraft_data['MTOW']/aircraft_data['MZFW_B']
aircraft_data['Ratio C']= 0.935*aircraft_data['MTOW']/aircraft_data['MZFW_C']
#aircraft_data['Ratio B']= (aircraft_data['MTOW']-6)/aircraft_data['MZFW_B']
#aircraft_data['Ratio C']= (aircraft_data['MTOW']-6)/aircraft_data['MZFW_C']
breguet = aircraft_data

g = 9.81
avg_velocity = 240 #m/s which is approximately 0.82 Mach
breguet['Ratio B']=breguet['Ratio B'].apply(np.log)
breguet['Ratio C']=breguet['Ratio C'].apply(np.log)

breguet['K_B']= 1852* breguet['RANGE_B']/breguet['Ratio B']
breguet['K_C']= 1852* breguet['RANGE_C']/breguet['Ratio C']
breguet['K']=(breguet['K_B']+breguet['K_C'])/2
breguet = breguet.merge(engines, left_on='Name', right_on='Name')
breguet['A'] = breguet['K']*g*0.001*breguet['TSFC Cruise']


breguet['L/D estimate'] = breguet['A']/avg_velocity

print(breguet[['Name','K', 'L/D estimate']])

fig = plt.figure(dpi=150)

# Add a subplot
ax = fig.add_subplot(1, 1, 1)


# Plot the dataframes with different symbols
ax.scatter(breguet['YOI'], breguet['L/D estimate'], marker='o', label='Aircraft')

for i, row in breguet.iterrows():
    plt.annotate(row['Name'], (row['YOI'], row['L/D estimate']),fontsize=6, xytext=(-8, 5), textcoords='offset points')
ax.legend()
xlabel = 'Year'
ylabel ='L/D'

plot.plot_layout(None, xlabel, ylabel, ax)
#plt.savefig('L_over_D_estimation_approach.png')

