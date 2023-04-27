import matplotlib.pyplot as plt
from structural.not_maintained import aircraft_type
from tools import plot

new_aircrafts = aircraft_type.type()
new_aircrafts['PL/OEW'] = (new_aircrafts['MZFW']-new_aircrafts['OEW'])/new_aircrafts['OEW']
new_aircrafts['MTOW/MZFW'] = new_aircrafts['MTOW']/new_aircrafts['MZFW']
new_aircrafts = new_aircrafts.dropna(subset='PL/OEW')

medium_aircrafts = new_aircrafts.loc[(new_aircrafts['Type']=='Narrow')]
large_aircrafts = new_aircrafts.loc[(new_aircrafts['Type']=='Wide')]
regional_aircrafts = new_aircrafts.loc[(new_aircrafts['Type']=='Regional')]

# Add a subplot
fig = plt.figure(dpi=300)
y_label = 'PL/OEW'
x_label = 'Year'

ax = fig.add_subplot(1, 1, 1)
ax.scatter(large_aircrafts['YOI'], large_aircrafts['PL/OEW'], marker='s',color='orange', label='Widebody')
ax.scatter(medium_aircrafts['YOI'], medium_aircrafts['PL/OEW'], marker='^',color='blue', label='Narrowbody')
ax.scatter(regional_aircrafts['YOI'], regional_aircrafts['PL/OEW'], marker='o',color='darkred', label='Regional Jets')

for i, row in large_aircrafts.iterrows():
    plt.annotate(row['Name'], (row['YOI'], row['PL/OEW']),
                 fontsize=6, xytext=(-10, 5),
                 textcoords='offset points')
    for i, row in medium_aircrafts.iterrows():
        plt.annotate(row['Name'], (row['YOI'], row['PL/OEW']),
                     fontsize=6, xytext=(-10, 5),
                     textcoords='offset points')

plot.plot_layout(None, x_label, y_label, ax)

plt.savefig('Graphs\pl_per_oew.png')

plt.show()

# Add a subplot
fig = plt.figure(dpi=300)
y_label = 'OEW/MTOW'
x_label = 'Year'

ax = fig.add_subplot(1, 1, 1)
ax.scatter(large_aircrafts['YOI'], large_aircrafts['OEW/MTOW'], marker='s',color='orange', label='Widebody')
ax.scatter(medium_aircrafts['YOI'], medium_aircrafts['OEW/MTOW'], marker='^',color='blue', label='Narrowbody')
ax.scatter(regional_aircrafts['YOI'], regional_aircrafts['OEW/MTOW'], marker='o',color='darkred', label='Regional Jets')

for i, row in large_aircrafts.iterrows():
    plt.annotate(row['Name'], (row['YOI'], row['OEW/MTOW']),
                 fontsize=6, xytext=(-10, 5),
                 textcoords='offset points')
    for i, row in medium_aircrafts.iterrows():
        plt.annotate(row['Name'], (row['YOI'], row['OEW/MTOW']),
                     fontsize=6, xytext=(-10, 5),
                     textcoords='offset points')

plot.plot_layout(None, x_label, y_label, ax)

plt.savefig('Graphs\oew_per_mtow.png')

plt.show()

# Add a subplot
fig = plt.figure(dpi=300)
y_label = 'MTOW/MZFW'
x_label = 'Year'

ax = fig.add_subplot(1, 1, 1)
ax.scatter(large_aircrafts['YOI'], large_aircrafts['MTOW/MZFW'], marker='s',color='orange', label='Widebody')
ax.scatter(medium_aircrafts['YOI'], medium_aircrafts['MTOW/MZFW'], marker='^',color='blue', label='Narrowbody')
ax.scatter(regional_aircrafts['YOI'], regional_aircrafts['MTOW/MZFW'], marker='o',color='darkred', label='Regional Jets')

for i, row in large_aircrafts.iterrows():
    plt.annotate(row['Name'], (row['YOI'], row['MTOW/MZFW']),
                 fontsize=6, xytext=(-10, 5),
                 textcoords='offset points')
    for i, row in medium_aircrafts.iterrows():
        plt.annotate(row['Name'], (row['YOI'], row['MTOW/MZFW']),
                     fontsize=6, xytext=(-10, 5),
                     textcoords='offset points')

plot.plot_layout(None, x_label, y_label, ax)

plt.savefig('Graphs\mtow_per_mzfw.png')

plt.show()