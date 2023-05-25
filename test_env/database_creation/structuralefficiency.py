import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from test_env.tools import plot

def calculate(savefig, folder_path):
    aircrafts = pd.read_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\Databank.xlsx')
    aircrafts['OEW/Exit Limit'] = aircrafts['OEW'] / aircrafts['Exit Limit']
    aircrafts['OEW/MTOW_2'] = aircrafts['OEW'] / aircrafts['MTOW']
    aircrafts['Composites'] = aircrafts['Composites'].fillna(0)
    CFR = 1.55  # g/cm^2
    alu2024t3 = 2.78  # g/cm^2
    aircrafts['Composite OEW'] = aircrafts['OEW']/2 + aircrafts['OEW']/2*(CFR/(aircrafts['Composites']*CFR+(1-aircrafts['Composites'])*alu2024t3))
    aircrafts['Composites Exit Limit'] = aircrafts['Composite OEW'] / aircrafts['Exit Limit']
    aircrafts.to_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\Databank.xlsx',  index=False)
    aircrafts = aircrafts.dropna(subset=['OEW/Exit Limit', 'OEW/MTOW_2'])
    aircrafts = aircrafts.groupby(['Name','Type','YOI'], as_index=False).agg({'OEW/Exit Limit':'mean', 'OEW/MTOW_2':'mean', 'OEW':'mean', 'Composites Exit Limit':'mean'})
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

    #large_aircrafts['OEW/m^2'] = large_aircrafts['OEW/Pax']/1.05
    #medium_aircrafts['OEW/m^2'] = medium_aircrafts['OEW/Pax']/1.48
    #years = pd.Series(range(1955, 2024))
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

    oew = pd.Series(np.arange(0, 200000))
    z = np.polyfit(aircrafts['OEW'],  aircrafts['OEW/MTOW_2'], 1)
    p = np.poly1d(z)
    # Add a subplot
    ax = fig.add_subplot(1, 1, 1)
    ax.scatter(large_aircrafts['OEW']/1000, large_aircrafts['OEW/MTOW_2'], marker='s',color='orange', label='Widebody')
    ax.scatter(medium_aircrafts['OEW']/1000, medium_aircrafts['OEW/MTOW_2'], marker='^',color='blue', label='Narrowbody')
    ax.scatter(regional_aircrafts['OEW']/1000, regional_aircrafts['OEW/MTOW_2'], marker='o',color='darkred', label='Regional Jets')
    ax.plot(oew/1000, p(oew),color='turquoise', label='Linear Regression')
    #for i, row in new_aircrafts.iterrows():
        #plt.annotate(row['Name'], (row['OEW'], row['Exit Limit']),
            #         fontsize=6, xytext=(-10, 5), textcoords='offset points')

    equation_text = f'y = {z[0]:.1e}x + {z[1]:.1e}'
    ax.text(0.15,0.15, equation_text, fontsize=12, color='black', transform=fig.transFigure)

    plot.plot_layout(None, x_label, y_label, ax)

    #_______PLOT OEW/EXITLIMIT WIDEBODY________

    fig = plt.figure(dpi=300)
    y_label = 'OEW[kg]/Pax Exit Limit'
    x_label = 'Year'

    # Add a subplot
    ax = fig.add_subplot(1, 1, 1)

    ax.scatter(large_aircrafts['YOI'], large_aircrafts['OEW/Exit Limit'], marker='s',color='orange', label='Widebody')
    ax.scatter(large_aircrafts['YOI'], large_aircrafts['Composites Exit Limit'], marker='s', color='red', label='100% Comp')
    ax.plot(x_large, p_large(x_large), color='orange', label='Linear Regression Narrow')

    for i, row in large_aircrafts.iterrows():
        plt.annotate(row['Name'], (row['YOI'], row['OEW/Exit Limit']),
                     fontsize=6, xytext=(-10, 5),
                     textcoords='offset points')

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
    ax.scatter(medium_aircrafts['YOI'], medium_aircrafts['Composites Exit Limit'], marker='^', color='green',label='100% Comp')
    ax.plot(x_medium, p_medium(x_medium), color='blue', label='Linear Regression Narrow')
    for i, row in medium_aircrafts.iterrows():
        plt.annotate(row['Name'], (row['YOI'], row['OEW/Exit Limit']),
                     fontsize=6, xytext=(-10, 5),
                     textcoords='offset points')
    for i, row in regional_aircrafts.iterrows():
        plt.annotate(row['Name'], (row['YOI'], row['OEW/Exit Limit']),
                     fontsize=6, xytext=(-10, 5),
                     textcoords='offset points')

    ax.legend()
    plt.xlim(1955, 2025)
    plt.xticks(np.arange(1955, 2024, 10))

    xlabel = 'Year'
    ylabel = 'OEW[kg]/Pax Exit Limit'

    plot.plot_layout(None, xlabel, ylabel, ax)
    if savefig:
        plt.savefig(folder_path+'/narrowbodyaircrafts.png')

    #_______PLOT EXITLIMIT VS OEW________

    fig = plt.figure(dpi=300)

    oew = pd.Series(np.arange(0, 200000))
    z = np.polyfit(aircrafts['OEW'],  aircrafts['OEW/Exit Limit'], 1)
    p = np.poly1d(z)
    # Add a subplot
    ax = fig.add_subplot(1, 1, 1)
    ax.scatter(large_aircrafts['OEW']/1000, large_aircrafts['OEW/Exit Limit'], marker='s',color='orange', label='Widebody')
    ax.scatter(medium_aircrafts['OEW']/1000, medium_aircrafts['OEW/Exit Limit'], marker='^',color='blue', label='Narrowbody')
    ax.scatter(regional_aircrafts['OEW']/1000, regional_aircrafts['OEW/Exit Limit'], marker='o',color='darkred', label='Regional Jets')
    ax.plot(oew/1000, p(oew),color='turquoise', label='Linear Regression')
    #for i, row in new_aircrafts.iterrows():
        #plt.annotate(row['Name'], (row['OEW'], row['Exit Limit']),
            #         fontsize=6, xytext=(-10, 5), textcoords='offset points')

    equation_text = f'y = {z[0]:.2e}x + {z[1]:.2e}'
    ax.text(0.4,0.15, equation_text, fontsize=12, color='black', transform=fig.transFigure)
    ax.legend()

    # Set the x and y axis labels
    ax.set_xlabel('OEW[kt]')
    ax.set_ylabel('OEW[kg]/Pax Exit Limit')

    ax.grid(which='major', axis='y', linestyle='-', linewidth = 0.5)
    ax.grid(which='minor', axis='y', linestyle='--', linewidth = 0.5)
    ax.grid(which='major', axis='x', linestyle='-', linewidth = 0.5)
    #if savefig:
        #plt.savefig('Graphs\exit_limit_vs_oew.png')

    #_______PLOT EXITLIMIT VS OEW________

    #fig = plt.figure(dpi=300)

    #range = pd.Series(np.arange(0, 16000))
    #z = np.polyfit(aircrafts['Range'],  aircrafts['OEW/MTOW_2'], 1)
    #p = np.poly1d(z)
    # Add a subplot
    #ax = fig.add_subplot(1, 1, 1)
    #ax.scatter(large_aircrafts['Range'], large_aircrafts['OEW/MTOW_2'], marker='s',color='orange', label='Widebody')
    #ax.scatter(medium_aircrafts['Range'], medium_aircrafts['OEW/MTOW_2'], marker='^',color='blue', label='Narrowbody')
    #ax.scatter(regional_aircrafts['Range'], regional_aircrafts['OEW/MTOW_2'], marker='o',color='darkred', label='Regional Jets')
    #ax.plot(range, p(range),color='turquoise', label='Linear Regression')
    #for i, row in new_aircrafts.iterrows():
        #plt.annotate(row['Name'], (row['OEW'], row['Exit Limit']),
            #         fontsize=6, xytext=(-10, 5), textcoords='offset points')

    #equation_text = f'y = {z[0]:.2e}x + {z[1]:.2e}'
    #ax.text(0.15,0.2, equation_text, fontsize=12, color='black', transform=fig.transFigure)
    #ax.legend(loc='upper left')
    # Add a legend to the plot
    #ax.legend()

    #Arrange plot size
    #plt.ylim(0, 600)
    #plt.xlim(0, 200)
    #plt.xticks(np.arange(1955, 2024, 10))

    # Set the x and y axis labels
    #ax.set_xlabel('Range [km]')
    #ax.set_ylabel('OEW/MTOW')

    #ax.grid(which='major', axis='y', linestyle='-', linewidth = 0.5)
    #ax.grid(which='minor', axis='y', linestyle='--', linewidth = 0.5)
    #ax.grid(which='major', axis='x', linestyle='-', linewidth = 0.5)
    # Set the plot title
    #ax.set_title('Overall Efficiency')
    #if savefig:
        #plt.savefig('Graphs/range_vs_mtow.png')
    #if plotfig:
        #plt.show()



    # PAX/OEW per YOI
    fig = plt.figure(dpi=300)


    # Add a subplot
    ax = fig.add_subplot(1, 1, 1)
    ax.scatter(large_aircrafts['YOI'], large_aircrafts['OEW/Exit Limit'], marker='s',color='orange', label='Widebody')
    ax.scatter(medium_aircrafts['YOI'], medium_aircrafts['OEW/Exit Limit'], marker='^',color='blue', label='Narrowbody')
    ax.scatter(regional_aircrafts['YOI'], regional_aircrafts['OEW/Exit Limit'], marker='o',color='darkred', label='Regional Jets')
    ax.plot(x_all, p_all(x_all), color='black', label='Linear Regression')
    #ax.plot(oew/1000, p(oew),color='turquoise', label='Linear Regression')
    #for i, row in new_aircrafts.iterrows():
        #plt.annotate(row['Name'], (row['OEW'], row['Exit Limit']),
            #         fontsize=6, xytext=(-10, 5), textcoords='offset points')

    ax.legend(loc='upper left')
    # Add a legend to the plot
    ax.legend()

    #Arrange plot size
    plt.ylim(0, 400)
    plt.xlim(1955, 2020)

    xlabel = 'Year'
    ylabel = 'OEW[kg]/Pax Exit Limit'
    plot.plot_layout(None, xlabel, ylabel, ax)
    if savefig:
        plt.savefig(folder_path+'/exit_limit_vs_year.png')


