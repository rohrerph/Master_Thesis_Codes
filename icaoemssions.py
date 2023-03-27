import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

# DATAFRAME PREPARATION
emissions_df = pd.read_excel(r"C:\Users\PRohr\Desktop\Masterarbeit\Data\edb-emissions-databank_v29 (web).xlsx", sheet_name='Gaseous Emissions and Smoke')
emissions_df['TSFC T/O']= emissions_df['Fuel Flow T/O (kg/sec)']/emissions_df['Rated Thrust (kN)']

emissions_df['Final Test Date']= pd.to_datetime(emissions_df['Final Test Date'])
emissions_df['Final Test Date']= emissions_df['Final Test Date'].dt.strftime('%Y')

yearly_emissions = emissions_df[['Final Test Date', 'Fuel Flow T/O (kg/sec)', 'B/P Ratio', 'Pressure Ratio', 'Rated Thrust (kN)','TSFC T/O']]
yearly_emissions = yearly_emissions.dropna()

#-------------------TSFC-------------------------
x = yearly_emissions['Final Test Date']
y = yearly_emissions['TSFC T/O']

fig = plt.figure(dpi=120)
# Add a subplot
ax = fig.add_subplot(1, 1, 1)

x_int = x.astype(np.int64)
years = pd.Series(range(1970, 2024))
z = np.polyfit(x_int, y, 1)
p = np.poly1d(z)

ax.scatter(x_int,y,label='TSFC T/O')
ax.plot(years, p(years),'-r')
plt.savefig('icao_takeoff_tsfc.png')
ax.legend()

plt.show()

#----------------------PRESSURE RATIO---------------

x = yearly_emissions['Final Test Date']
y = yearly_emissions['Pressure Ratio']

fig = plt.figure(dpi=120)

# Add a subplot
ax = fig.add_subplot(1, 1, 1)

x_int = x.astype(np.int64)
years = pd.Series(range(1970, 2024))
z = np.polyfit(x_int, y, 1)
p = np.poly1d(z)

ax.scatter(x_int,y, label='Pressure Ratio')
ax.plot(years, p(years),'-r')
ax.legend()
plt.savefig('icao_pressureratio.png')
plt.show()

#------------------ B/P Ratio ------------------------

x = yearly_emissions['Final Test Date']
y = yearly_emissions['B/P Ratio']

fig = plt.figure(dpi=120)

# Add a subplot
ax = fig.add_subplot(1, 1, 1)

x_int = x.astype(np.int64)
years = pd.Series(range(1970, 2024))
z = np.polyfit(x_int, y, 1)
p = np.poly1d(z)

ax.scatter(x_int,y, label='B/P Ratio')
ax.plot(years, p(years), '-r')
ax.legend()
plt.savefig('icao_bypassratio.png')
plt.show()
