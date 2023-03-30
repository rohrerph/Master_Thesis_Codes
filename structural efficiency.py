import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#This file is just a draft to see how the structural efficiency in the 2000s evolved

babikian_aircrafts = pd.read_excel(r"C:\Users\PRohr\Desktop\Masterarbeit\Data\Aircraft Databank.xlsx", sheet_name='Data Table')
babikian_aircrafts = babikian_aircrafts.loc[babikian_aircrafts['Still in new Metric']=='Yes']
not_babikian_aircrafts = babikian_aircrafts.loc[babikian_aircrafts['Babikian']=='No']
babikian_aircrafts = babikian_aircrafts.loc[babikian_aircrafts['Babikian']=='Yes']

#Data retrieved by me from Janes all Aircrafts and Manufacturers website.
new_aircrafts = pd.read_excel(r"C:\Users\PRohr\Desktop\Masterarbeit\Data\Aircraft Databank.xlsx", sheet_name='New Data Entry')
new_aircrafts = new_aircrafts.dropna(axis='columns')


new_aircrafts = new_aircrafts.groupby(['Company', 'Name','YOI']).agg({'OEW':'mean', 'MTOW':'mean'})
new_aircrafts['OEW/MTOW'] = new_aircrafts['OEW']/new_aircrafts['MTOW']

aircrafts_added = pd.merge(not_babikian_aircrafts,new_aircrafts, on=['Company','Name','YOI'], suffixes=('_drop', ''))
aircrafts_added = aircrafts_added.drop('OEW/MTOW_drop', axis=1)

babikian_aircrafts_total = babikian_aircrafts.append(aircrafts_added)

babikian_aircrafts_total.to_excel('Aircraft Databank v2.xlsx')

babikian_aircrafts = babikian_aircrafts[['Name','YOI','OEW/MTOW']]
aircrafts_added = aircrafts_added[['Name','YOI','OEW/MTOW']]

all_together = babikian_aircrafts.append(aircrafts_added)
all_together = all_together.dropna(subset='OEW/MTOW')

x_int = aircrafts_added['YOI'].astype(np.int64)
years = pd.Series(range(1990, 2024))
z = np.polyfit(x_int,  aircrafts_added['OEW/MTOW'], 1)
p = np.poly1d(z)

x_int_all = all_together['YOI'].astype(np.int64)
years_all = pd.Series(range(1965, 2024))
z_all = np.polyfit(x_int_all,  all_together['OEW/MTOW'], 2)
p_all = np.poly1d(z_all)

fig = plt.figure(dpi=150)

# Add a subplot
ax = fig.add_subplot(1, 1, 1)

# Plot the dataframes with different symbols
ax.scatter(babikian_aircrafts['YOI'], babikian_aircrafts['OEW/MTOW'], marker='o', label='Babikian')
ax.scatter(aircrafts_added['YOI'], aircrafts_added['OEW/MTOW'], marker='^', label='Added')
ax.plot(years, p(years),'-r', label='Added Linear Fit')
ax.plot(years_all, p_all(years_all),'-b', label='Overall Second Order')

for i, row in babikian_aircrafts.iterrows():
    plt.annotate(row['Name'], (row['YOI'], row['OEW/MTOW']),fontsize=6, xytext=(-8, 5), textcoords='offset points')
for i, row in aircrafts_added.iterrows():
    plt.annotate(row['Name'], (row['YOI'], row['OEW/MTOW']),fontsize=6, xytext=(-8, 5), textcoords='offset points')

#Arrange plot size
plt.ylim(0.4, 0.7)
plt.xlim(1965, 2020)
plt.xticks(np.arange(1965, 2020, 10))

# Set the x and y axis labels
ax.set_xlabel('Year')
ax.set_ylabel('OEW/MTOW')

# Set the plot title
ax.set_title('Structural Efficiency')
ax.legend()

# Show the plot
plt.savefig('StructuralEfficiency_Update3.png')
plt.show()
