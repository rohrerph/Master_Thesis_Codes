import pandas as pd

data = pd.read_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\overall\data\Databank2.xlsx')

flight_speed = 240 #m/s

#use metric from the book Aircraft Propulsion and Gas Turbine Engines per turbine
data['Air Mass Core'] = data['Air Mass Flow [kg/s]']/data['B/P Ratio']
data['Air Mass Fan'] = data['Air Mass Flow [kg/s]'] - data['Air Mass Core']
data['f'] = 0.5*data['Fuel Flow [kg/s]']/data['Air Mass Flow [kg/s]']
data['Velocity Fan'] = (0.75*0.5*data['Dmax'])/data['Air Mass Fan'] + flight_speed
data['Velocity Core'] = ((0.25*0.5*data['Dmax']/data['Air Mass Core']) + flight_speed) / (1+data['f'])

data['nominator']= 2*flight_speed*(((data['f']+1)*data['Velocity Core']-flight_speed) + data['B/P Ratio']*(data['Velocity Fan']-flight_speed))
data['denominator']= ((1+data['f'])*data['Velocity Core']**2-flight_speed**2)+data['B/P Ratio']*(data['Velocity Fan']**2-flight_speed**2)
data['prop_eff'] = data['nominator']/data['denominator']

data['nominator_thermal']= data['Air Mass Core']*((1+data['f'])*data['Velocity Core']**2-flight_speed**2)+data['Air Mass Fan']*(data['Velocity Fan']**2-flight_speed**2)
data['denominator_thermal'] = (data['Fuel Flow [kg/s]']*43.1*10**6)
data['thermal_eff'] = data['nominator_thermal']/data['denominator_thermal']
data['ovr_eff_calc'] = data['thermal_eff']*data['prop_eff']
data = data.dropna(subset='thermal_eff')

#method from Kurzke
# dmax divided by two, because there are two engines each with this mass stream
data['v_exhaust'] = data['Dmax']*0.5/data['Air Mass Flow [kg/s]'] + flight_speed
data['nu_prop'] = (2*flight_speed)/(data['v_exhaust']+flight_speed)
data['nu_therm'] = data['Engine Efficiency']/data['nu_prop']
data = data[['Name', 'Engine', 'Air Mass Fan', 'Air Mass Core', 'thermal_eff', 'prop_eff', 'ovr_eff_calc', 'Engine Efficiency', 'nu_prop', 'nu_therm']]


#best method probably nu therm via nu prop as other values seem far to small . and there has to be a lot of calibration done, how much thrust is produced by the core and the fan

data = data.groupby(['Name', 'Engine'], as_index=False).agg({'thermal_eff':'mean', 'prop_eff':'mean', 'ovr_eff':'mean', 'ovr_eff_calc':'mean'})
#results in overestimation therm eff and underestimation of prop eff
#more or less accurate values when we half the max continuous thrust, how much continuous thrust is used for steady cruise. ?

