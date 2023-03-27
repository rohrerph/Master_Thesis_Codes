import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_excel(r"C:\Users\PRohr\Desktop\Masterarbeit\Data\Aircraft Databank v2.xlsx", sheet_name='New Data Entry')

#Locate turbofan database book from Roux
roux = data.loc[(data['Source cruise TSFC']==data['Source TO TSFC']) & (data['Source cruise TSFC']!='Janes Aeroengines')]
janes = data.loc[(data['Source cruise TSFC']==data['Source TO TSFC']) & (data['Source cruise TSFC']=='Janes Aeroengines')]
all = data.loc[data['Source cruise TSFC']==data['Source TO TSFC']]
all = all.groupby(['Engine']).agg({'Engine TSFC cruise [g/kNs]':'mean','Engine TSFC take off [g/kNs]':'mean' })
roux = roux.drop_duplicates(subset='Engine')
janes = janes.drop_duplicates(subset='Engine')

#-------------------TAKE OFF vs CRUISE-------------------------

y_roux = roux['Engine TSFC cruise [g/kNs]']
x_roux = roux['Engine TSFC take off [g/kNs]']
y_janes = janes['Engine TSFC cruise [g/kNs]']
x_janes = janes['Engine TSFC take off [g/kNs]']
y_all = all['Engine TSFC cruise [g/kNs]']
x_all = all['Engine TSFC take off [g/kNs]']


fig = plt.figure(dpi=120)
# Add a subplot
ax = fig.add_subplot(1, 1, 1)


z_roux = np.polyfit(x_roux, y_roux, 1)
p_roux = np.poly1d(z_roux)
z_janes = np.polyfit(x_janes, y_janes, 1)
p_janes = np.poly1d(z_janes)
z_all = np.polyfit(x_all, y_all, 1)
p_all = np.poly1d(z_all)

ax.scatter(x_roux,y_roux, label='Cruise vs. T/O Roux')
ax.scatter(x_janes,y_janes, label='Cruise vs. T/O Janes')
ax.plot(x_roux, p_roux(x_roux), label='Roux')
ax.plot(x_janes, p_janes(x_janes), label='Janes')
ax.plot(x_all, p_all(x_all), label='Combined')

equation_text = f'y = {z_all[0]:.2f}x + {z_all[1]:.2f}'
#Polynom obtained by Lee et al. was 0.869x + 8.65 here we have 0.84x + 8.49 which is quite similar.
ax.text(0.6,0.15, equation_text, fontsize=12, color='black', transform=fig.transFigure)

#plt.savefig('takeoff_vs_cruise_tsfc.png')
ax.legend()

plt.show()

