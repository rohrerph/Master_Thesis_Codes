import pandas as pd
from not_maintained.tools import plot, dict
import matplotlib.pyplot as plt

#load dictionaries
airplanes_dict = dict.AirplaneModels().get_models()
aircraftnames = dict.AircraftNames().get_aircraftnames()
airplanes = airplanes_dict.keys()
airlines = dict.USAirlines().get_airlines()


#Data from December 2022, is also monthly available back to 1990.
T100 = pd.read_csv(r"C:\Users\PRohr\Desktop\Masterarbeit\Data\T_T100_SEGMENT_US_CARRIER_ONLY.csv")
AC_types = pd.read_csv(r"C:\Users\PRohr\Desktop\Masterarbeit\Data\L_AIRCRAFT_TYPE (1).csv")

T100 = T100.loc[T100['CARRIER_GROUP'] == 3]
# subgroup 1 for aircraft passenger configuration
T100 = T100.loc[T100['AIRCRAFT_CONFIG'] == 1]
# Use the 19 Airlines
T100 = T100.loc[T100['UNIQUE_CARRIER_NAME'].isin(airlines)]
T100 = pd.merge(T100, AC_types, left_on='AIRCRAFT_TYPE', right_on='Code')
T100 = T100.loc[T100['Description'].isin(airplanes)]
T100 = T100.loc[T100['DISTANCE']>=0]
T100['SEATS']=T100['SEATS']/T100['DEPARTURES_PERFORMED']
km = 1.60934
T100['DISTANCE'] = T100['DISTANCE']*km
T100['Calc PAYLOAD'] = T100['PASSENGERS']*100 + T100['PAYLOAD']*0.453592
#T100 = T100.loc[T100['PAYLOAD']>=0]

Boeing_737_900 = T100.loc[T100['Description'].isin(['Boeing 737-900', 'Boeing 737-900ER'])]
kg = 0.453592
Boeing_737_900['Calc PAYLOAD'] = Boeing_737_900['Calc PAYLOAD']*kg/Boeing_737_900['DEPARTURES_PERFORMED']
#Boeing_737_900['DISTANCE']= Boeing_737_900['DISTANCE']/Boeing_737_900['DEPARTURES_PERFORMED']

Boeing_737_900_standard= Boeing_737_900.loc[Boeing_737_900['Description']=='Boeing 737-900']
Boeing_737_900_standard['Calc PAYLOAD'] = Boeing_737_900_standard['Calc PAYLOAD']+42901
Boeing_737_900_longrange = Boeing_737_900.loc[Boeing_737_900['Description']=='Boeing 737-900ER']
Boeing_737_900_longrange['Calc PAYLOAD'] = Boeing_737_900_longrange['Calc PAYLOAD']+44677

payload_lr = [67721, 67721, 66678, 51700, 44677, 44677]  # payload in kg
range_km_lr = [0, 3238, 4070, 8970, 10000, 0]  # range in km

payload_sr = [62732, 62732, 58060, 42902, 42902]  # payload in kg
range_km_sr = [0, 3700, 5180, 6600, 0]  # range in km
# Plot the payload range diagram



# Add a subplot
fig = plt.figure(dpi=300)
y_label = 'Payload'
x_label = 'Range'

ax = fig.add_subplot(1, 1, 1)
ax.scatter(Boeing_737_900_standard['DISTANCE'], Boeing_737_900_standard['Calc PAYLOAD'], marker='s', s=3, color='orange', label='Boeing 737-900')
ax.scatter(Boeing_737_900_longrange['DISTANCE'], Boeing_737_900_longrange['Calc PAYLOAD'], marker='^', s=3, color='blue', label='Boeing 737-900ER')
ax.plot( range_km_lr, payload_lr, color = 'blue')
ax.plot( range_km_sr, payload_sr, color = 'orange')
plot.plot_layout(None, x_label, y_label, ax)

plt.savefig('Graphs\payload_vs_range_b737.png')


#Airbus
a319 = T100.loc[T100['Description'].isin(['Airbus Industrie A319'])]
kg = 0.453592
a319['Calc PAYLOAD'] = a319['Calc PAYLOAD']*kg/a319['DEPARTURES_PERFORMED']


# Add a subplot
fig = plt.figure(dpi=300)
y_label = 'Payload'
x_label = 'Range'

ax = fig.add_subplot(1, 1, 1)
ax.scatter(a319['DISTANCE'], a319['Calc PAYLOAD'], marker='s',color='orange', label='A319')

plot.plot_layout(None, x_label, y_label, ax)



plt.savefig('Graphs\payload_vs_range_a319.png')

plt.show()

#this gives the actual number of seats across the whole us fleet!
T100 = T100.groupby(['Description'], as_index=False).agg({'SEATS':'mean'})