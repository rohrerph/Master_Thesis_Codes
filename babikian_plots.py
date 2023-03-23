import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

engine = pd.read_excel(r"C:\Users\PRohr\OneDrive\Desktop\Data Extraction 2.xlsx", sheet_name='Figure 3')
structure = pd.read_excel(r"C:\Users\PRohr\OneDrive\Desktop\Data Extraction 2.xlsx", sheet_name='Figure 4')
aerodyn = pd.read_excel(r"C:\Users\PRohr\OneDrive\Desktop\Data Extraction 2.xlsx", sheet_name='Figure 5')
overall = pd.read_excel(r"C:\Users\PRohr\OneDrive\Desktop\Data Extraction 2.xlsx", sheet_name='Figure 2')

#Plot SFC
engine_turboprops = engine.iloc[:, 0:3]
engine_turboprops.columns = engine_turboprops.iloc[0]
engine_turboprops = engine_turboprops[1:].dropna()

engine_regional = engine.iloc[:, 4:7]
engine_regional.columns = engine_regional.iloc[0]
engine_regional = engine_regional[1:].dropna()

engine_large = engine.iloc[:, 8:11]
engine_large.columns = engine_large.iloc[0]
engine_large = engine_large[1:]


fig = plt.figure()

# Add a subplot
ax = fig.add_subplot(1, 1, 1)

# Plot the dataframes with different symbols
ax.scatter(engine_regional['Year'], engine_regional['TSFC (mg/Ns)'], marker='o', label='Regional Jets')
ax.scatter(engine_turboprops['Year'], engine_turboprops['TSFC (mg/Ns)'], marker='s', label='Turboprops')
ax.scatter(engine_large['Year'], engine_large['TSFC (mg/Ns)'], marker='^', label='Large Jets')

# Add labels to each point
for i, row in engine_regional.iterrows():
    plt.annotate(row['Label'], (row['Year'], row['TSFC (mg/Ns)']),fontsize=6, xytext=(-8, 5), textcoords='offset points')
for i, row in engine_turboprops.iterrows():
    plt.annotate(row['Label'], (row['Year'], row['TSFC (mg/Ns)']),fontsize=6, xytext=(-8, 5), textcoords='offset points')
for i, row in engine_large.iterrows():
    plt.annotate(row['Label'], (row['Year'], row['TSFC (mg/Ns)']),fontsize=6, xytext=(-8, 5), textcoords='offset points')

# Add a legend to the plot
ax.legend()

#Arrange plot size
plt.ylim(0, 30)
plt.xlim(1955, 2005)
plt.xticks(np.arange(1955, 2006, 5))

# Set the x and y axis labels
ax.set_xlabel('Year')
ax.set_ylabel('TSFC (mg/Ns)')

# Set the plot title
ax.set_title('Engine Efficiency')

# Show the plot
plt.savefig('BabikianEngineEfficiency.png')
plt.show()


#Aero
aerodyn_turboprops = aerodyn.iloc[:, 0:3]
aerodyn_turboprops.columns = aerodyn_turboprops.iloc[0]
aerodyn_turboprops = aerodyn_turboprops[1:].dropna()

aerodyn_regional = aerodyn.iloc[:, 4:7]
aerodyn_regional.columns = aerodyn_regional.iloc[0]
aerodyn_regional = aerodyn_regional[1:].dropna()

aerodyn_large = aerodyn.iloc[:, 8:11]
aerodyn_large.columns = aerodyn_large.iloc[0]
aerodyn_large = aerodyn_large[1:].dropna()

fig = plt.figure()

# Add a subplot
ax = fig.add_subplot(1, 1, 1)

# Plot the dataframes with different symbols
ax.scatter(aerodyn_regional['Year'], aerodyn_regional['L/Dmax'], marker='o', label='Regional Jets')
ax.scatter(aerodyn_turboprops['Year'], aerodyn_turboprops['L/Dmax'], marker='s', label='Turboprops')
ax.scatter(aerodyn_large['Year'], aerodyn_large['L/Dmax'], marker='^', label='Large Jets')

# Add labels to each point
for i, row in aerodyn_regional.iterrows():
    plt.annotate(row['Label'], (row['Year'], row['L/Dmax']),fontsize=6, xytext=(-8, 5), textcoords='offset points')
for i, row in aerodyn_turboprops.iterrows():
    plt.annotate(row['Label'], (row['Year'], row['L/Dmax']),fontsize=6, xytext=(-8, 5), textcoords='offset points')
for i, row in aerodyn_large.iterrows():
    plt.annotate(row['Label'], (row['Year'], row['L/Dmax']),fontsize=6, xytext=(-8, 5), textcoords='offset points')

# Add a legend to the plot
ax.legend()

#Arrange plot size
plt.ylim(0, 25)
plt.xlim(1955, 2005)
plt.xticks(np.arange(1955, 2006, 5))

# Set the x and y axis labels
ax.set_xlabel('Year')
ax.set_ylabel('L/Dmax')

# Set the plot title
ax.set_title('Aerodynamic Efficiency')

# Show the plot
plt.savefig('BabikianAerodynamicEfficiency.png')
plt.show()


#Structure
structure_turboprops = structure.iloc[:, 0:3]
structure_turboprops.columns = structure_turboprops.iloc[0]
structure_turboprops = structure_turboprops[1:].dropna()

structure_regional = structure.iloc[:, 4:7]
structure_regional.columns = structure_regional.iloc[0]
structure_regional = structure_regional[1:].dropna()

structure_large = structure.iloc[:, 8:11]
structure_large.columns = structure_large.iloc[0]
structure_large = structure_large[1:].dropna()

fig = plt.figure()

# Add a subplot
ax = fig.add_subplot(1, 1, 1)

# Plot the dataframes with different symbols
ax.scatter(structure_regional['Year'], structure_regional['OEW/MTOW'], marker='o', label='Regional Jets')
ax.scatter(structure_turboprops['Year'], structure_turboprops['OEW/MTOW'], marker='s', label='Turboprops')
ax.scatter(structure_large['Year'], structure_large['OEW/MTOW'], marker='^', label='Large Jets')

# Add labels to each point
for i, row in structure_regional.iterrows():
    plt.annotate(row['Label'], (row['Year'], row['OEW/MTOW']),fontsize=6, xytext=(-8, 5), textcoords='offset points')
for i, row in structure_turboprops.iterrows():
    plt.annotate(row['Label'], (row['Year'], row['OEW/MTOW']),fontsize=6, xytext=(-8, 5), textcoords='offset points')
for i, row in structure_large.iterrows():
    plt.annotate(row['Label'], (row['Year'], row['OEW/MTOW']),fontsize=6, xytext=(-8, 5), textcoords='offset points')

# Add a legend to the plot
ax.legend()

#Arrange plot size
plt.ylim(0, 0.7)
plt.xlim(1955, 2005)
plt.xticks(np.arange(1955, 2006, 5))

# Set the x and y axis labels
ax.set_xlabel('Year')
ax.set_ylabel('OEW/MTOW')

# Set the plot title
ax.set_title('Structural Efficiency')

# Show the plot
plt.savefig('BabikianStructuralEfficiency.png')
plt.show()


#overall
overall_large = overall.iloc[:, 0:2]
overall_large.columns = overall_large.iloc[0]
overall_large = overall_large[1:].dropna()

overall_regional = overall.iloc[:, 3:5]
overall_regional.columns = overall_regional.iloc[0]
overall_regional = overall_regional[1:].dropna()

overall_large_fleet = overall.iloc[:, 6:8]
overall_large_fleet.columns = overall_large_fleet.iloc[0]
overall_large_fleet = overall_large_fleet[1:].dropna()

overall_regional_fleet = overall.iloc[:, 9:11]
overall_regional_fleet.columns = overall_regional_fleet.iloc[0]
overall_regional_fleet = overall_regional_fleet[1:].dropna()

fig = plt.figure()

# Add a subplot
ax = fig.add_subplot(1, 1, 1)

# Plot the dataframes with different symbols
ax.scatter(overall_large['Year'], overall_large['EU (MJ/ASK)'], marker='^', label='Large Aircraft')
ax.scatter(overall_regional['Year'], overall_regional['EU (MJ/ASK)'], marker='s', label='Regional Aircraft')
ax.plot(overall_large_fleet['Year'], overall_large_fleet['EU (MJ/ASK)'], label='Large Aircraft Fleet')
ax.plot(overall_regional_fleet['Year'], overall_regional_fleet['EU (MJ/ASK)'], label='Large Aircraft Fleet')

# Add a legend to the plot
ax.legend()

#Arrange plot size
plt.ylim(0, 5)
plt.xlim(1955, 2005)
plt.xticks(np.arange(1955, 2006, 5))

# Set the x and y axis labels
ax.set_xlabel('Year')
ax.set_ylabel('EU (MJ/ASK)')

# Set the plot title
ax.set_title('Overall Efficiency')

# Show the plot
plt.savefig('BabikianOverallEfficiency.png')
plt.show()

