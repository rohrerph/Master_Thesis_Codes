import pandas as pd
import matplotlib.pyplot as plt
from test_env.tools import plot
import numpy as np
def calculate(savefig, folder_path):
    aircrafts = pd.read_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\Databank.xlsx')
    aircrafts = aircrafts[['Company',
                           'Name',
                           'Type',
                           'YOI',
                           'MTOW,integer,kilogram',
                           'MZFW,integer,kilogram',
                           'Exit Limit',
                           'Fuel capacity,integer,litre',
                           'TSFC Cruise',
                           'Engine Efficiency',
                           'EU (MJ/ASK)',
                           'OEW/Exit Limit',
                           'L/D estimate',
                           'Aspect Ratio',
                           'k',
                           'Wingspan,float,metre',
                           'prop_eff',
                           'thermal_eff',
                           'c_L',
                           'c_D',
                           'c_Di',
                           'c_D0',
                           'EU_estimate',
                           'Pax',
                           'Height,float,metre',
                           'B/P Ratio',
                           'Overcome Thrust']]
    aircrafts['EU_estimate_Limit'] = aircrafts['EU_estimate']*aircrafts['Pax']/aircrafts['Exit Limit']
    aircrafts = aircrafts.groupby(['Company','Name','Type','YOI'], as_index=False).agg('mean')
    print(' --> [CREATE AIRCRAFT DATABASE]: Compare Energy Usage from US DOT with Breguet Range Equation')

    # Plot EU estimate from Breguet Range Equation vs the Actual EU from the US DOT
    fig = plt.figure(dpi=150)

    # Add a subplot
    ax = fig.add_subplot(1, 1, 1)
    # Plot the dataframes with different symbols
    ax.scatter(aircrafts['YOI'], aircrafts['EU_estimate'], marker='o', label='Breguet Range Equation')
    ax.scatter(aircrafts['YOI'], aircrafts['EU_estimate_Limit'], marker='s', label='Breguet Range Equation, Exit Limit')
    ax.scatter(aircrafts['YOI'], aircrafts['EU (MJ/ASK)'], marker='^', label='US DOT')

    ax.legend()
    xlabel = 'Year'
    ylabel ='Energy Usage EU (MJ/ASK)'

    plot.plot_layout(None, xlabel, ylabel, ax)
    if savefig:
        plt.savefig(folder_path+'/energyusage.png')

    # Plot EU estimate from Breguet Range Equation vs the Actual EU from the US DOT
    fig = plt.figure(dpi=150)
    bpr = aircrafts[['YOI', 'B/P Ratio', 'TSFC Cruise',]]
    low = bpr.loc[bpr['B/P Ratio']<=4]
    medium = bpr.loc[(bpr['B/P Ratio']>=4) & (bpr['B/P Ratio']<=8)]
    high = bpr.loc[bpr['B/P Ratio']>=8]

    # Add a subplot
    ax = fig.add_subplot(1, 1, 1)
    # Plot the dataframes with different symbols
    ax.scatter(low['YOI'], low['TSFC Cruise'],color='red', label='BPR <4')
    ax.scatter(medium['YOI'], medium['TSFC Cruise'], color='purple', label='BPR 4-8')
    ax.scatter(high['YOI'], high['TSFC Cruise'], color='blue', label='BPR >8')
    ax.legend()
    xlabel = 'Year'
    ylabel ='TSFC Cruise'

    plot.plot_layout(None, xlabel, ylabel, ax)
    if savefig:
        plt.savefig(folder_path+'/bypassratiogroups.png')

    aircrafts.to_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\Databank.xlsx', index=False)





