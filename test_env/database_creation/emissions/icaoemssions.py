import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np


def calculate(z):
    # DATAFRAME PREPARATION
    emissions_df = pd.read_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\database_creation\rawdata\emissions\edb-emissions-databank_v29 (web).xlsx', sheet_name='Gaseous Emissions and Smoke')
    emissions_df['TSFC T/O']= emissions_df['Fuel Flow T/O (kg/sec)']/emissions_df['Rated Thrust (kN)']*1000

    emissions_df['Final Test Date']= pd.to_datetime(emissions_df['Final Test Date'])
    emissions_df['Final Test Date']= emissions_df['Final Test Date'].dt.strftime('%Y')

    yearly_emissions = emissions_df[['Engine Identification','Final Test Date', 'Fuel Flow T/O (kg/sec)', 'B/P Ratio', 'Pressure Ratio', 'Rated Thrust (kN)','TSFC T/O']]
    yearly_emissions = yearly_emissions.dropna()

    poly = lambda x: z[0]*x + z[1]

    yearly_emissions['TSFC Cruise'] = yearly_emissions['TSFC T/O'].apply(poly)
    yearly_emissions.to_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\database_creation\rawdata\emissions\icao_cruise_emissions.xlsx')


