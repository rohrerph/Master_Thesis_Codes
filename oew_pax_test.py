import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Data retrieved by me from Janes all Aircrafts and Manufacturers website.
new_aircrafts = pd.read_excel(r"C:\Users\PRohr\Desktop\Masterarbeit\Data\Aircraft Databank.xlsx", sheet_name='New Data Entry')
new_aircrafts = new_aircrafts.dropna(axis='columns')



new_aircrafts = new_aircrafts.groupby(['Name'], as_index=False).agg({'OEW':'mean', 'MTOW':'mean', 'Pax':'mean', 'YOI':'mean'})
new_aircrafts['OEW/Pax'] = new_aircrafts['OEW']/new_aircrafts['Pax']
new_aircrafts['OEW/MTOW'] = new_aircrafts['OEW']/new_aircrafts['MTOW']

#ICAO Wake cateogries
large_aircrafts = new_aircrafts.loc[(new_aircrafts['MTOW']>= 136000)]
medium_aircrafts = new_aircrafts.loc[(new_aircrafts['MTOW']<= 136000)]

fig, axs = plt.subplots(1, 2, figsize=(10, 4))


# Plot the dataframes with different symbols
axs[0].scatter(large_aircrafts['YOI'], large_aircrafts['OEW/Pax'], marker='o', label='Large Aircrafts')
axs[0].scatter(medium_aircrafts['YOI'], medium_aircrafts['OEW/Pax'], marker='o', label='Medium Aircrafts')
axs[0].set_xlabel('Year')
axs[0].set_ylabel('OEW/Pax')

axs[1].scatter(large_aircrafts['YOI'], large_aircrafts['OEW/MTOW'], marker='o', label='OEW/MTOW Large')
axs[1].scatter(medium_aircrafts['YOI'], medium_aircrafts['OEW/MTOW'], marker='o', label='Medium Aircrafts')
axs[1].set_xlabel('Year')
axs[1].set_ylabel('OEW/MTOW')

for i, row in large_aircrafts.iterrows():
    axs[0].annotate(row['Name'], (row['YOI'], row['OEW/Pax']),fontsize=6, xytext=(-8, 5), textcoords='offset points')
    axs[1].annotate(row['Name'], (row['YOI'], row['OEW/MTOW']), fontsize=6, xytext=(-8, 5), textcoords='offset points')
for i, row in medium_aircrafts.iterrows():
    axs[0].annotate(row['Name'], (row['YOI'], row['OEW/Pax']),fontsize=6, xytext=(-8, 5), textcoords='offset points')
    axs[1].annotate(row['Name'], (row['YOI'], row['OEW/MTOW']), fontsize=6, xytext=(-8, 5), textcoords='offset points')

#Arrange plot size
#plt.ylim(0, 0.7)
#plt.xlim(1955, 2020)
#plt.xticks(np.arange(1955, 2020, 10))


axs[0].legend()
axs[1].legend()

# Set the plot title
axs[0].set_title('OEW per Passenger')
axs[1].set_title('OEW per MTOW')
# Show the plot
plt.savefig('oew_per_pax_and_mtow.png')
plt.show()
