import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

savefig = True
plotfig = False
my_values = False

#Data retrieved by me from Janes all Aircrafts and Manufacturers website.
new_aircrafts = pd.read_excel(r"C:\Users\PRohr\Desktop\Masterarbeit\Data\Aircraft Databank v2.xlsx", sheet_name='New Data Entry')
babikian = pd.read_excel(r"C:\Users\PRohr\Desktop\Masterarbeit\Data\Aircraft Databank v2.xlsx", sheet_name='Data Table')
babikian = babikian.loc[babikian['Babikian']=='Yes']

if my_values:
    babikian = babikian[['Name', 'YOI', 'Exit Limit', 'OEW','MTOW','Type']]
    babikian['OEW/MTOW']= babikian['OEW']/babikian['MTOW']
else:
    babikian = babikian[['Name', 'YOI', 'Exit Limit', 'OEW/MTOW','OEW', 'Type']]
babikian['OEW/Pax'] = babikian['OEW'] / babikian['Exit Limit']
new_aircrafts = new_aircrafts.groupby(['Name','Type'], as_index=False).agg({'OEW':'mean', 'MTOW':'mean', 'Exit Limit':'mean', 'YOI':'mean', 'Range':'mean'})
new_aircrafts['OEW/Pax'] = new_aircrafts['OEW']/new_aircrafts['Exit Limit']
new_aircrafts['OEW/MTOW'] = new_aircrafts['OEW']/new_aircrafts['MTOW']
new_aircrafts = new_aircrafts.append(babikian)
new_aircrafts = new_aircrafts.dropna(subset='OEW/MTOW')

new_aircrafts.loc[new_aircrafts['Exit Limit'] < 100, 'Type'] = 'Regional'

medium_aircrafts = new_aircrafts.loc[(new_aircrafts['Type']=='Narrow')]
large_aircrafts = new_aircrafts.loc[(new_aircrafts['Type']=='Wide')]
regional_aircrafts = new_aircrafts.loc[(new_aircrafts['Type']=='Regional')]

#large_aircrafts['OEW/m^2'] = large_aircrafts['OEW/Pax']/1.05
#medium_aircrafts['OEW/m^2'] = medium_aircrafts['OEW/Pax']/1.48

years = pd.Series(range(1955, 2024))
x_large = large_aircrafts['YOI'].astype(np.int64)
y_large = large_aircrafts['OEW/Pax'].astype(np.float64)
z_large = np.polyfit(x_large,  y_large, 1)
p_large = np.poly1d(z_large)
x_medium = medium_aircrafts['YOI'].astype(np.int64)
y_medium = medium_aircrafts['OEW/Pax'].astype(np.float64)
z_medium = np.polyfit(x_medium,  y_medium, 1)
p_medium = np.poly1d(z_medium)

x_all = new_aircrafts['YOI'].astype(np.int64)
y_all = new_aircrafts['OEW/Pax'].astype(np.float64)
z_all = np.polyfit(x_all,  y_all, 1)
p_all = np.poly1d(z_all)

#_______PLOT OEW/MTOW VS OEW________

fig = plt.figure(dpi=300)

oew = pd.Series(range(0, 200000))
z = np.polyfit(new_aircrafts['OEW'],  new_aircrafts['OEW/MTOW'], 1)
p = np.poly1d(z)
# Add a subplot
ax = fig.add_subplot(1, 1, 1)
ax.scatter(large_aircrafts['OEW']/1000, large_aircrafts['OEW/MTOW'], marker='s',color='orange', label='Widebody')
ax.scatter(medium_aircrafts['OEW']/1000, medium_aircrafts['OEW/MTOW'], marker='^',color='blue', label='Narrowbody')
ax.scatter(regional_aircrafts['OEW']/1000, regional_aircrafts['OEW/MTOW'], marker='o',color='darkred', label='Regional Jets')
ax.plot(oew/1000, p(oew),color='turquoise', label='Linear Regression')
#for i, row in new_aircrafts.iterrows():
    #plt.annotate(row['Name'], (row['OEW'], row['Exit Limit']),
        #         fontsize=6, xytext=(-10, 5), textcoords='offset points')

equation_text = f'y = {z[0]:.1e}x + {z[1]:.1e}'
ax.text(0.15,0.15, equation_text, fontsize=12, color='black', transform=fig.transFigure)
ax.legend(loc='upper left')
# Add a legend to the plot
ax.legend()

#Arrange plot size
#plt.ylim(0, 600)
#plt.xlim(0, 200)
#plt.xticks(np.arange(1955, 2024, 10))

# Set the x and y axis labels
ax.set_ylabel('OEW/MTOW')
ax.set_xlabel('OEW[kt]')

ax.grid(which='major', axis='y', linestyle='-', linewidth = 0.5)
ax.grid(which='minor', axis='y', linestyle='--', linewidth = 0.5)
ax.grid(which='major', axis='x', linestyle='-', linewidth = 0.5)
# Set the plot title
#ax.set_title('Overall Efficiency')
if savefig:
    plt.savefig('oewmtow_vs_oew.png')

#_______PLOT OEW/EXITLIMIT WIDEBODY________

fig = plt.figure(dpi=300)

# Add a subplot
ax = fig.add_subplot(1, 1, 1)

ax.scatter(large_aircrafts['YOI'], large_aircrafts['OEW/Pax'], marker='s',color='orange', label='Widebody')
ax.plot(x_large, p_large(x_large), color='orange', label='Linear Regression Narrow')

for i, row in large_aircrafts.iterrows():
    plt.annotate(row['Name'], (row['YOI'], row['OEW/Pax']),
                 fontsize=6, xytext=(-10, 5),
                 textcoords='offset points')

# Add a legend to the plot
#ax.legend()

#Arrange plot size
#plt.ylim(0, 4)
plt.xlim(1955, 2025)
plt.xticks(np.arange(1955, 2024, 10))

# Set the x and y axis labels
ax.set_xlabel('Year')
ax.set_ylabel('OEW[kg]/Pax Exit Limit')

ax.grid(which='major', axis='y', linestyle='-', linewidth = 0.5)
ax.grid(which='minor', axis='y', linestyle='--', linewidth = 0.5)
ax.grid(which='major', axis='x', linestyle='-', linewidth = 0.5)
# Set the plot title
#ax.set_title('Overall Efficiency')
if savefig:
    plt.savefig('widebody_aircrafts.png')




#_______PLOT OEW/EXITLIMIT NARROWBODY________

fig = plt.figure(dpi=300)

# Add a subplot
ax = fig.add_subplot(1, 1, 1)

ax.scatter(regional_aircrafts['YOI'], regional_aircrafts['OEW/Pax'], marker='o',color='darkred', label='Regional Jets')
ax.scatter(medium_aircrafts['YOI'], medium_aircrafts['OEW/Pax'], marker='^',color='blue', label='Narrowbody')
ax.plot(x_medium, p_medium(x_medium), color='blue', label='Linear Regression Narrow')
for i, row in medium_aircrafts.iterrows():
    plt.annotate(row['Name'], (row['YOI'], row['OEW/Pax']),
                 fontsize=6, xytext=(-10, 5),
                 textcoords='offset points')
for i, row in regional_aircrafts.iterrows():
    plt.annotate(row['Name'], (row['YOI'], row['OEW/Pax']),
                 fontsize=6, xytext=(-10, 5),
                 textcoords='offset points')

# Add a legend to the plot

#Arrange plot size
#plt.ylim(0, 4)
plt.xlim(1955, 2025)
plt.xticks(np.arange(1955, 2024, 10))

# Set the x and y axis labels
ax.set_xlabel('Year')
ax.set_ylabel('OEW[kg]/Pax Exit Limit')

ax.grid(which='major', axis='y', linestyle='-', linewidth = 0.5)
ax.grid(which='minor', axis='y', linestyle='--', linewidth = 0.5)
ax.grid(which='major', axis='x', linestyle='-', linewidth = 0.5)
# Set the plot title
#ax.set_title('Overall Efficiency')
if savefig:
    plt.savefig('mediumaircrafts.png')

#_______PLOT EXITLIMIT VS OEW________

fig = plt.figure(dpi=300)

oew = pd.Series(range(0, 200000))
z = np.polyfit(new_aircrafts['OEW'],  new_aircrafts['OEW/Pax'], 1)
p = np.poly1d(z)
# Add a subplot
ax = fig.add_subplot(1, 1, 1)
ax.scatter(large_aircrafts['OEW']/1000, large_aircrafts['OEW/Pax'], marker='s',color='orange', label='Widebody')
ax.scatter(medium_aircrafts['OEW']/1000, medium_aircrafts['OEW/Pax'], marker='^',color='blue', label='Narrowbody')
ax.scatter(regional_aircrafts['OEW']/1000, regional_aircrafts['OEW/Pax'], marker='o',color='darkred', label='Regional Jets')
ax.plot(oew/1000, p(oew),color='turquoise', label='Linear Regression')
#for i, row in new_aircrafts.iterrows():
    #plt.annotate(row['Name'], (row['OEW'], row['Exit Limit']),
        #         fontsize=6, xytext=(-10, 5), textcoords='offset points')

equation_text = f'y = {z[0]:.2e}x + {z[1]:.2e}'
ax.text(0.4,0.15, equation_text, fontsize=12, color='black', transform=fig.transFigure)
ax.legend(loc='upper left')
# Add a legend to the plot
ax.legend()

#Arrange plot size
#plt.ylim(0, 600)
#plt.xlim(0, 200)
#plt.xticks(np.arange(1955, 2024, 10))

# Set the x and y axis labels
ax.set_xlabel('OEW[kt]')
ax.set_ylabel('OEW[kg]/Pax Exit Limit')

ax.grid(which='major', axis='y', linestyle='-', linewidth = 0.5)
ax.grid(which='minor', axis='y', linestyle='--', linewidth = 0.5)
ax.grid(which='major', axis='x', linestyle='-', linewidth = 0.5)
# Set the plot title
#ax.set_title('Overall Efficiency')
if savefig:
    plt.savefig('exit_limit_vs_oew.png')

#_______PLOT EXITLIMIT VS OEW________

fig = plt.figure(dpi=300)

range = pd.Series(range(0, 16000))
new_aircrafts = new_aircrafts.dropna(subset='Range')
z = np.polyfit(new_aircrafts['Range'],  new_aircrafts['OEW/MTOW'], 1)
p = np.poly1d(z)
# Add a subplot
ax = fig.add_subplot(1, 1, 1)
ax.scatter(large_aircrafts['Range'], large_aircrafts['OEW/MTOW'], marker='s',color='orange', label='Widebody')
ax.scatter(medium_aircrafts['Range'], medium_aircrafts['OEW/MTOW'], marker='^',color='blue', label='Narrowbody')
ax.scatter(regional_aircrafts['Range'], regional_aircrafts['OEW/MTOW'], marker='o',color='darkred', label='Regional Jets')
ax.plot(range, p(range),color='turquoise', label='Linear Regression')
#for i, row in new_aircrafts.iterrows():
    #plt.annotate(row['Name'], (row['OEW'], row['Exit Limit']),
        #         fontsize=6, xytext=(-10, 5), textcoords='offset points')

equation_text = f'y = {z[0]:.2e}x + {z[1]:.2e}'
ax.text(0.15,0.2, equation_text, fontsize=12, color='black', transform=fig.transFigure)
ax.legend(loc='upper left')
# Add a legend to the plot
ax.legend()

#Arrange plot size
#plt.ylim(0, 600)
#plt.xlim(0, 200)
#plt.xticks(np.arange(1955, 2024, 10))

# Set the x and y axis labels
ax.set_xlabel('Range [km]')
ax.set_ylabel('OEW/MTOW')

ax.grid(which='major', axis='y', linestyle='-', linewidth = 0.5)
ax.grid(which='minor', axis='y', linestyle='--', linewidth = 0.5)
ax.grid(which='major', axis='x', linestyle='-', linewidth = 0.5)
# Set the plot title
#ax.set_title('Overall Efficiency')
if savefig:
    plt.savefig('range_vs_mtow.png')
if plotfig:
    plt.show()
