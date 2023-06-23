import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from test_env.database_creation.tools import plot


def calculate(savefig, folder_path):
    aircrafts = pd.read_excel(r'Databank.xlsx')
    aircrafts['OEW/Exit Limit'] = aircrafts['OEW'] / aircrafts['Exit Limit']
    aircrafts['OEW/Pax'] = aircrafts['OEW'] / aircrafts['Pax']
    aircrafts['OEW/MTOW_2'] = aircrafts['OEW'] / aircrafts['MTOW']
    aircrafts['Composites'] = aircrafts['Composites'].fillna(0)
    aircrafts.to_excel(r'Databank.xlsx', index=False)

    # Calculate the min weight which could be obtained using 100% composite materials for a Boeing 787-10 Dreamliner
    CFR = 1.55  # g/cm^2
    alu2024t3 = 2.78  # g/cm^2
    steel = 8 # g/cm^2
    titanium = 4.48 #g/cm^2
    other = 8 # assume heaviest material for possibly biggest OEW decrease
    oew_b787 = aircrafts.loc[aircrafts['Name']=='787-10 Dreamliner', 'OEW'].iloc[0]
    exit_b787 = aircrafts.loc[aircrafts['Name'] == '787-10 Dreamliner', 'Exit Limit'].iloc[0]
    oew_exit_b777 = aircrafts.loc[aircrafts['Name'] == '777-300/300ER/333ER', 'OEW/Exit Limit'].iloc[0]
    oew_b787_composites = (oew_b787/exit_b787) * (CFR) / (CFR*0.52+alu2024t3*0.2+steel*0.07+other*0.07+titanium*0.14)

    aircrafts['Composite OEW'] = aircrafts['OEW']*(CFR/(aircrafts['Composites']*CFR+(1-aircrafts['Composites'])*alu2024t3))
    aircrafts['Composites Exit Limit'] = aircrafts['Composite OEW'] / aircrafts['Exit Limit']
    aircrafts = aircrafts.dropna(subset=['OEW/Exit Limit', 'OEW/MTOW_2'])
    aircrafts = aircrafts.groupby(['Name','Type','YOI'], as_index=False).agg({'OEW/Exit Limit':'mean', 'OEW/MTOW_2':'mean', 'OEW':'mean', 'Composites Exit Limit':'mean', 'OEW/Pax':'mean'})
    medium_aircrafts = aircrafts.loc[(aircrafts['Type']=='Narrow')]
    large_aircrafts = aircrafts.loc[(aircrafts['Type']=='Wide')]
    regional_aircrafts = aircrafts.loc[(aircrafts['Type']=='Regional')]

    #linear regression for all aircraft to see how overall structural efficiency has increased.
    x_all = aircrafts['YOI'].astype(np.int64)
    y_all = aircrafts['OEW/Exit Limit'].astype(np.float64)
    z_all = np.polyfit(x_all,  y_all, 1)
    intercept = z_all[1]
    slope = z_all[0]
    predicted_y = slope * x_all + intercept
    data = {'x': x_all, 'y': y_all, 'predicted_y': predicted_y}
    data = pd.DataFrame(data)
    p_all = np.poly1d(z_all)
    x_large = large_aircrafts['YOI'].astype(np.int64)
    y_large = large_aircrafts['OEW/Exit Limit'].astype(np.float64)
    z_large = np.polyfit(x_large,  y_large, 1)
    p_large = np.poly1d(z_large)
    x_medium = medium_aircrafts['YOI'].astype(np.int64)
    y_medium = medium_aircrafts['OEW/Exit Limit'].astype(np.float64)
    z_medium = np.polyfit(x_medium,  y_medium, 1)
    p_medium = np.poly1d(z_medium)

    #_______PLOT OEW/MTOW VS OEW________

    fig = plt.figure(dpi=300)
    y_label = 'OEW/MTOW'
    x_label = 'OEW[kt]'

    oew = pd.Series(np.arange(0, 275000))
    z = np.polyfit(aircrafts['OEW'],  aircrafts['OEW/MTOW_2'], 1)
    p = np.poly1d(z)
    # Add a subplot
    ax = fig.add_subplot(1, 1, 1)
    ax.scatter(large_aircrafts['OEW']/1000, large_aircrafts['OEW/MTOW_2'], marker='s',color='orange', label='Widebody')
    ax.scatter(medium_aircrafts['OEW']/1000, medium_aircrafts['OEW/MTOW_2'], marker='^',color='blue', label='Narrowbody')
    ax.scatter(regional_aircrafts['OEW']/1000, regional_aircrafts['OEW/MTOW_2'], marker='o',color='darkred', label='Regional Jets')
    #ax.plot(oew/1000, p(oew),color='black', label='Linear Regression')
    #for i, row in new_aircrafts.iterrows():
        #plt.annotate(row['Name'], (row['OEW'], row['Exit Limit']),
            #         fontsize=6, xytext=(-10, 5), textcoords='offset points')

    #equation_text = f'y = {z[0]:.1e}x + {z[1]:.1e}'
    #ax.text(0.15,0.15, equation_text, fontsize=12, color='black', transform=fig.transFigure)
    ax.legend()
    plot.plot_layout(None, x_label, y_label, ax)
    if savefig:
        plt.savefig(folder_path+'\oewmtow_vs_oew.png')

    #_______PLOT OEW/EXITLIMIT WIDEBODY________

    fig = plt.figure(dpi=300)
    y_label = 'OEW[kg]/Pax Exit Limit'
    x_label = 'Aircraft Year of Introduction'

    # Add a subplot
    ax = fig.add_subplot(1, 1, 1)

    ax.scatter(large_aircrafts['YOI'], large_aircrafts['OEW/Exit Limit'], marker='s',color='orange', label='Widebody')
    #ax.scatter(large_aircrafts['YOI'], large_aircrafts['Composites Exit Limit'], marker='s', color='red', label='100% Comp')
    ax.axhline(y=oew_exit_b777*0.8, color='black', linestyle='--', linewidth=2, label='Physical Limitation')
    ax.plot(x_large, p_large(x_large), color='orange')
    plt.annotate('NASA ERA Project', (1960, oew_exit_b777*0.8),
                    fontsize=6, xytext=(-10, 5),
                    textcoords='offset points')
    #for i, row in large_aircrafts.iterrows():
     #   plt.annotate(row['Name'], (row['YOI'], row['OEW/Exit Limit']),
      #               fontsize=6, xytext=(-10, 5),
       #              textcoords='offset points')

    #plt.ylim(0, 4)
    plt.xlim(1955, 2025)
    plt.xticks(np.arange(1955, 2024, 10))

    plot.plot_layout(None, x_label, y_label, ax)
    ax.legend()
    # Set the plot title
    #ax.set_title('Overall Efficiency')
    if savefig:
        plt.savefig(folder_path+'\widebody_aircrafts.png')

    #_______PLOT OEW/EXITLIMIT NARROWBODY________

    fig = plt.figure(dpi=300)

    # Add a subplot
    ax = fig.add_subplot(1, 1, 1)

    ax.scatter(regional_aircrafts['YOI'], regional_aircrafts['OEW/Exit Limit'], marker='o',color='darkred', label='Regional Jets')
    ax.scatter(medium_aircrafts['YOI'], medium_aircrafts['OEW/Exit Limit'], marker='^',color='blue', label='Narrowbody')
    ax.plot(x_medium, p_medium(x_medium), color='blue')
    #for i, row in medium_aircrafts.iterrows():
     #   plt.annotate(row['Name'], (row['YOI'], row['OEW/Exit Limit']),
      #               fontsize=6, xytext=(-10, 5),
       #              textcoords='offset points')
    #for i, row in regional_aircrafts.iterrows():
     #   plt.annotate(row['Name'], (row['YOI'], row['OEW/Exit Limit']),
      #               fontsize=6, xytext=(-10, 5),
       #              textcoords='offset points')

    ax.legend()
    plt.xlim(1955, 2025)
    plt.xticks(np.arange(1955, 2024, 10))

    xlabel = 'Aircraft Year of Introduction'
    ylabel = 'OEW[kg]/Pax Exit Limit'

    plot.plot_layout(None, xlabel, ylabel, ax)
    if savefig:
        plt.savefig(folder_path+'/narrowbodyaircrafts.png')

    #_______PLOT EXITLIMIT VS OEW________

    fig = plt.figure(dpi=300)

    z = np.polyfit(aircrafts['OEW'],  aircrafts['OEW/Exit Limit'], 1)
    p = np.poly1d(z)
    # Add a subplot
    ax = fig.add_subplot(1, 1, 1)
    ax.scatter(large_aircrafts['OEW']/1000, large_aircrafts['OEW/Exit Limit'], marker='s',color='orange', label='Widebody')
    ax.scatter(medium_aircrafts['OEW']/1000, medium_aircrafts['OEW/Exit Limit'], marker='^',color='blue', label='Narrowbody')
    ax.scatter(regional_aircrafts['OEW']/1000, regional_aircrafts['OEW/Exit Limit'], marker='o',color='darkred', label='Regional Jets')
    #ax.plot(oew/1000, p(oew),color='black', label='Linear Regression')
    #for i, row in new_aircrafts.iterrows():
        #plt.annotate(row['Name'], (row['OEW'], row['Exit Limit']),
            #         fontsize=6, xytext=(-10, 5), textcoords='offset points')

    #equation_text = f'y = {z[0]:.2e}x + {z[1]:.2e}'
    #ax.text(0.4,0.15, equation_text, fontsize=12, color='black', transform=fig.transFigure)
    ax.legend()

    # Set the x and y axis labels
    xlabel='OEW[kt]'
    ylabel='OEW[kg]/Pax Exit Limit'
    plot.plot_layout(None, xlabel, ylabel, ax)
    if savefig:
        plt.savefig(folder_path+'/exit_limit_vs_oew.png')

    # PAX/OEW per YOI
    fig = plt.figure(dpi=300)
    ax = fig.add_subplot(1, 1, 1)

    ax.scatter(large_aircrafts['YOI'], large_aircrafts['OEW/Exit Limit'], marker='s',color='orange', label='Widebody')
    ax.scatter(medium_aircrafts['YOI'], medium_aircrafts['OEW/Exit Limit'], marker='^',color='blue', label='Narrowbody')
    ax.scatter(regional_aircrafts['YOI'], regional_aircrafts['OEW/Exit Limit'], marker='o',color='darkred', label='Regional Jets')
    ax.plot(x_large, p_large(x_large), color='orange')
    ax.plot(x_medium, p_medium(x_medium), color='blue')
    plt.annotate('A330-900', (2018, 299), fontsize=8, xytext=(-10, -10), textcoords='offset points')
    plt.annotate('B787-10', (2018, 308), fontsize=8, xytext=(-10, 5), textcoords='offset points')

    ax.legend(loc='upper left')
    # Add a legend to the plot
    ax.legend()

    #Arrange plot size
    plt.ylim(0, 400)
    plt.xlim(1955, 2020)

    xlabel = 'Aircraft Year of Introduction'
    ylabel = 'OEW[kg]/Pax Exit Limit'
    plot.plot_layout(None, xlabel, ylabel, ax)
    if savefig:
        plt.savefig(folder_path+'/exit_limit_vs_year.png')

    #_______PLOT PAX VS OEW________
    fig = plt.figure(dpi=300)
    ax = fig.add_subplot(1, 1, 1)

    ax.scatter(large_aircrafts['YOI'], large_aircrafts['OEW/Pax'], marker='s',color='orange', label='Widebody')
    ax.scatter(medium_aircrafts['YOI'], medium_aircrafts['OEW/Pax'], marker='^',color='blue', label='Narrowbody')
    ax.scatter(regional_aircrafts['YOI'], regional_aircrafts['OEW/Pax'], marker='o',color='darkred', label='Regional Jets')
    #ax.axhline(y=232, color='black', linestyle='-', linewidth=2, label='Theoretical Limit for TW')
    ax.legend(loc='upper left')
    # Add a legend to the plot
    ax.legend()

    #Arrange plot size
    plt.ylim(0, 600)
    plt.xlim(1955, 2020)

    xlabel = 'Aircraft Year of Introduction'
    ylabel = 'OEW[kg]/Pax'
    plot.plot_layout(None, xlabel, ylabel, ax)
    if savefig:
        plt.savefig(folder_path+'/pax_vs_year.png')


