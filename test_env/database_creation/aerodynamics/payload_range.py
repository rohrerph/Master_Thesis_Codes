import pandas as pd
from test_env.database_creation.tools import dict, plot
import geopandas as gpd
from shapely.geometry import Point
from shapely.geometry import LineString
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
from scipy.stats import gaussian_kde

airplanes_dict = dict.AirplaneModels().get_models()
airplanes = airplanes_dict.keys()
airlines = dict.USAirlines().get_airlines()

# Air time efficiency in 2022
AC_types = pd.read_csv(r"C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\database_creation\rawdata\USDOT\L_AIRCRAFT_TYPE (1).csv")
T100 = pd.read_csv(r"C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\database_creation\rawdata\USDOT\T_T100_SEGMENT_ALL_CARRIER_2022.csv")

# Use the 19 Airlines
T100 = T100.loc[T100['UNIQUE_CARRIER_NAME'].isin(airlines)]
T100 = pd.merge(T100, AC_types, left_on='AIRCRAFT_TYPE', right_on='Code')
T100 = T100.loc[T100['Description'].isin(airplanes)]
T100 = T100.loc[T100['AIR_TIME'] > 0]
T100["DISTANCE"] = T100["DISTANCE"] * 1.62
T100["PAYLOAD"] = T100["PAYLOAD"] * 0.4535
T100["PAYLOAD"] = T100["PAYLOAD"] / T100['DEPARTURES_PERFORMED'] / 1000
T100 = T100.loc[T100.index.repeat(T100['DEPARTURES_PERFORMED'])]
T100 = T100.reset_index(drop=True)

# Check for a 777-200 and an A320 and create the payload range diagrams.

a320 = T100.loc[T100['Description']=='Airbus Industrie A320-100/200']
b777 = T100.loc[T100['Description']=='Boeing 777-200ER/200LR/233LR']
a320_boundaries = {
    'Range': [0, 58.8, 76.5, 100],
    'Payload': [0, 0, 19.1, 100]}
a320_boundaries = pd.DataFrame(a320_boundaries)

mtow = 78
mzfw = np.linspace(42.6, 62.5, num=100)
mzfw_values = (0.94 * mtow / mzfw)
mzfw_values = np.log(mzfw_values)
range_values = np.linspace(0, 6800, num=100)
a320_tsfc = 16.984
speed = 240
g = 9.81

matrix = np.zeros((100, 100))
for i in range(100):
    for j in range(100):
        matrix[i, j] = range_values[i] /(mzfw_values[j]*1000)
matrix = matrix*g*a320_tsfc/240
matrix = pd.DataFrame(matrix)
matrix.columns = mzfw
matrix.index = range_values
matrix = matrix.T
matrix = np.where((matrix >= 5) & (matrix <= 25), matrix, np.nan)

# ATTENTION DOESNT MAKE SENSE ATT ALL AS ALAWYS MZFW IS CONSIDERED.
fig, ax = plt.subplots(dpi=300)

heatmap = plt.imshow(matrix[::-1], cmap='YlGnBu', aspect='auto')
contours = plt.contour(matrix[::-1], colors='black', linestyles='dashed', levels=10, linewidths=0.5)
plt.clabel(contours, inline=True, fontsize=8)
plt.colorbar(heatmap)
ax.plot(a320_boundaries['Range'], a320_boundaries['Payload'], label='Limit', color='black')
# Set labels
title = 'Lift-to-Drag Ratio'
xlabel = 'Distance'
ylabel = 'Payload'
plot.plot_layout(title, xlabel, ylabel, ax)
new_xticks = [0, 25, 50, 75, 100 ]
new_xlabels = ['0', '1700', '3400', '5100', '6800']
new_yticks = [0, 25, 50, 75, 100]
new_ylabels = ['19.9', '15', '10', '5', '0']
plt.yticks(new_yticks, new_ylabels)
plt.xticks(new_xticks, new_xlabels)


#A320 Plot
a320_boundaries = {
    'Range': [0, 4000, 5200, 6800],
    'Payload': [19.9, 19.9, 15.9, 0]}
a320_boundaries = pd.DataFrame(a320_boundaries)

fig, ax = plt.subplots(dpi=300)

# Calculate the heatmap data
heatmap, xedges, yedges = np.histogram2d(a320['DISTANCE'], a320['PAYLOAD'], bins=50)
extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

# Plot the heatmap
im = ax.imshow(heatmap.T, origin='lower', extent=extent, aspect='auto', cmap='YlOrRd')
ax.plot(a320_boundaries['Range'], a320_boundaries['Payload'], label='Limit', color='black')
# Set labels
title = 'Payload/Range Diagram'
xlabel = 'Distance'
ylabel = 'Payload'
plot.plot_layout(title, xlabel, ylabel, ax)
cbar = plt.colorbar(im)
plt.ylim(0,22)
plt.xlim(0,6900)
plt.show()

# PLOT 777-200 POTENTIALLY BETTER RESULTS

b777_boundaries = {
    'Range': [0, 14070, 15023, 17687],
    'Payload': [50.352, 50.352, 43.262, 0]}
b777_boundaries = pd.DataFrame(b777_boundaries)

fig, ax = plt.subplots(dpi=300)

# Calculate the heatmap data
heatmap, xedges, yedges = np.histogram2d(b777['DISTANCE'], b777['PAYLOAD'], bins=50)
extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

# Plot the heatmap
im = ax.imshow(heatmap.T, origin='lower', extent=extent, aspect='auto', cmap='YlOrRd')
ax.plot(b777_boundaries['Range'], b777_boundaries['Payload'], label='Limit', color='black')
# Set labels
title = 'Payload/Range Diagram'
xlabel = 'Distance'
ylabel = 'Payload'
plot.plot_layout(title, xlabel, ylabel, ax)
cbar = plt.colorbar(im)

plt.show()

