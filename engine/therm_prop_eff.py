import pandas as pd
import numpy as np
from tools import dict
from tools import T2_preprocessing
import math
import matplotlib.pyplot as plt




#use metric from the book Aircraft Propulsion and Gas Turbine Engines
data['Air Mass Core'] = data['Air mass flow [kg/s]']/data['B/P Ratio']
data['Air Mass Fan'] = data['Air mass flow [kg/s]'] - data['Air Mass Core']
data['f'] = data['Fuel Flow [kg/s]']/data['Air mass flow [kg/s]']
data['Velocity Fan'] = (0.75*data['Thrust assumption'])/data['Air Mass Fan'] + flight_speed
data['Velocity Core'] = ((0.25*data['Thrust assumption']/data['Air Mass Core']) + flight_speed) / (1+data['f'])

data['nominator']= 2*flight_speed*(((data['f']+1)*data['Velocity Core']-flight_speed) + data['B/P Ratio']*(data['Velocity Fan']-flight_speed))
data['denominator']= ((1+data['f'])*data['Velocity Core']**2-flight_speed**2)+data['B/P Ratio']*(data['Velocity Fan']**2-flight_speed**2)
data['prop_eff'] = data['nominator']/data['denominator']

data['nominator_thermal']= data['Air Mass Core']*((1+data['f'])*data['Velocity Core']**2-flight_speed**2)+data['Air Mass Fan']*(data['Velocity Fan']**2-flight_speed**2)
data['denominator_thermal'] = (2*data['Fuel Flow [kg/s]']*42.8*10**6)
data['thermal_eff'] = data['nominator_thermal']/data['denominator_thermal']
data['ovr_eff'] = flight_speed / (data['TSFC Cruise']* heating_value)
data['ovr_eff_calc'] = data['thermal_eff']*data['prop_eff']
data = data.groupby(['Name', 'Engine'], as_index=False).agg({'thermal_eff':'mean', 'prop_eff':'mean', 'ovr_eff':'mean', 'ovr_eff_calc':'mean'})
#more or less accurate values when we half the max continuous thrust, how much continuous thrust is used for steady cruise. ?

