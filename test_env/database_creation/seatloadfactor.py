import pandas as pd
import numpy as np
from test_env.tools import dict
from test_env.tools import T2_preprocessing
from test_env.tools import plot
import matplotlib.pyplot as plt

def calculate(savefig, folder_path):
    #load dictionaries
    airplanes_dict = dict.AirplaneModels().get_models()
    airplanes = airplanes_dict.keys()
    airlines = dict.USAirlines().get_airlines()

    airplane_types = dict.AirplaneTypes().get_types()
    airplane_types = pd.DataFrame({'Description': list(airplane_types.keys()), 'Type': list(airplane_types.values())})

    #Read Data, T2 is data from the US back to 1990, historic_slf contains data from the ICAO worldwide back to 1950
    T2 = pd.read_csv(r"C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\database_creation\rawdata\USDOT\T_SCHEDULE_T2.csv")
    AC_types = pd.read_csv(r"C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\database_creation\rawdata\USDOT\L_AIRCRAFT_TYPE (1).csv")
    historic_slf = pd.read_excel(r"C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\database_creation\rawdata\USDOT\Traffic and Operations 1929-Present_Vollständige D_data.xlsx")
    historic_slf = historic_slf.dropna(subset='PLF').reset_index()
    historic_slf['PLF'] = historic_slf['PLF'].str.replace(',', '.').astype(float)

    T2 = T2_preprocessing.preprocessing(T2, AC_types, airlines, airplanes)
    T2 = T2.merge(airplane_types)

    T2_annual = T2.groupby(['YEAR','Type'], as_index=False).agg({'SLF':'median','Airborne Eff.':'mean'})

    overall = T2.groupby(['YEAR'], as_index=False).agg({'SLF':'median','Airborne Eff.':'mean'})
    regional = T2_annual.loc[T2_annual['Type']=='Regional'].reset_index()
    narrow = T2_annual.loc[T2_annual['Type']=='Narrow'].reset_index()
    wide = T2_annual.loc[T2_annual['Type']=='Wide'].reset_index()

    #Regional jets were filtered out as it seems not much data is available and values therefore not very accurate

    #plot figures for slf
    fig = plt.figure(dpi=300)

    # Add a subplot
    ax = fig.add_subplot(1, 1, 1)
    x_label = 'Year'
    y_label = 'Seat Load Factor'

    ax.plot(historic_slf['Year'], historic_slf['PLF'],color='black')
    ax.plot(historic_slf['Year'][0], historic_slf['PLF'][0],color='black',marker='*', label='Worldwide')
    ax.plot(overall['YEAR'], overall['SLF'],color='turquoise')
    ax.plot(overall['YEAR'][0], overall['SLF'][0],color='turquoise',marker='o', label='US')
    ax.plot(wide['YEAR'], wide['SLF'],color='orange')
    ax.plot(wide['YEAR'][0], wide['SLF'][0],color='orange', marker='s', label='US Widebody')
    ax.plot(narrow['YEAR'], narrow['SLF'],color='blue')
    ax.plot(narrow['YEAR'][0], narrow['SLF'][0],color='blue',marker='^', label='US Narrowbody')
    ax.legend()

    #Arrange plot size
    plt.ylim(0, 1)
    plt.xlim(1948, 2023)
    plt.xticks(np.arange(1950, 2024, 10))

    plot.plot_layout(None, x_label, y_label, ax)
    if savefig:
        plt.savefig(folder_path+'/seatloadfactor.png')

    # Plot Figure for Airborne Efficiency
    fig = plt.figure(dpi=300)
    ax = fig.add_subplot(1, 1, 1)

    x_label = 'Year'
    y_label = 'Ratio'

    ax.plot(overall['YEAR'], overall['Airborne Eff.'],color='turquoise')
    ax.plot(overall['YEAR'][0], overall['Airborne Eff.'][0],color='turquoise',marker='o', label='Overall')
    ax.plot(wide['YEAR'], wide['Airborne Eff.'],color='orange')
    ax.plot(wide['YEAR'][0], wide['Airborne Eff.'][0],color='orange', marker='s', label='Widebody')
    ax.plot(narrow['YEAR'], narrow['Airborne Eff.'],color='blue')
    ax.plot(narrow['YEAR'][0], narrow['Airborne Eff.'][0],color='blue',marker='^', label='Narrowbody')
    ax.legend()

    #Arrange plot size
    plt.ylim(0, 1)
    plt.xlim(1990, 2023)
    plt.xticks(np.arange(1990, 2024, 5))

    plot.plot_layout(None, x_label, y_label, ax)
    if savefig:
        plt.savefig(folder_path+'/airborneefficiency.png')