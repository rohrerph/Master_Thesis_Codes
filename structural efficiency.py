import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#This file is just a draft to see how the structural efficiency in the 2000s evolved

babikian_aircrafts = pd.read_excel(r"C:\Users\PRohr\Desktop\Masterarbeit\Data\Aircraft Databank.xlsx", sheet_name='Data Table')
babikian_aircrafts = babikian_aircrafts.loc[babikian_aircrafts['Still in new Metric']=='Yes']
babikian_aircrafts_real = babikian_aircrafts.loc[babikian_aircrafts['Babikian']=='Yes']
babikian_aircrafts = babikian_aircrafts.loc[babikian_aircrafts['Babikian']=='No']
#Data retrieved by me from Janes all Aircrafts and Manufacturers website.
new_aircrafts = pd.read_excel(r"C:\Users\PRohr\Desktop\Masterarbeit\Data\Aircraft Databank.xlsx", sheet_name='New Data Entry')
new_aircrafts = new_aircrafts.dropna(axis='columns')


new_aircrafts = new_aircrafts.groupby(['Company', 'Name','YOI']).agg({'OEW':'mean', 'MTOW':'mean'})
new_aircrafts['OEW/MTOW'] = new_aircrafts['OEW']/new_aircrafts['MTOW']

aircrafts_added = pd.merge(babikian_aircrafts,new_aircrafts, on=['Company','Name','YOI'], suffixes=('_drop', ''))
aircrafts_added = aircrafts_added.drop('OEW/MTOW_drop', axis=1)

babikian_aircrafts_real = babikian_aircrafts_real.append(aircrafts_added)

babikian_aircrafts_real.to_excel('Aircraft Databank v2.xlsx')

plot_df = babikian_aircrafts_real[['Name','YOI','OEW/MTOW']]

fig = plt.figure()

# Add a subplot
ax = fig.add_subplot(1, 1, 1)

# Plot the dataframes with different symbols
ax.scatter(plot_df['YOI'], plot_df['OEW/MTOW'], marker='o', label='Aircrafts')
for i, row in plot_df.iterrows():
    plt.annotate(row['Name'], (row['YOI'], row['OEW/MTOW']),fontsize=6, xytext=(-8, 5), textcoords='offset points')

#Arrange plot size
plt.ylim(0, 0.7)
plt.xlim(1955, 2020)
plt.xticks(np.arange(1955, 2020, 10))

# Set the x and y axis labels
ax.set_xlabel('Year')
ax.set_ylabel('OEW/MTOW')

# Set the plot title
ax.set_title('Structural Efficiency')

# Show the plot
plt.savefig('StructuralEfficiency_Update.png')
plt.show()
