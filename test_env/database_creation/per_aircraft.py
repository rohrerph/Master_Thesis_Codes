import pandas as pd
def calculate():
    aircrafts = pd.read_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\Databank.xlsx')
    aircrafts = aircrafts[['Company',
                           'Name',
                           'Type',
                           'YOI',
                           'TSFC Cruise',
                           'Engine Efficiency',
                           'EU (MJ/ASK)',
                           'OEW/Exit Limit',
                           'L/D estimate',
                           'Aspect Ratio',
                           'k',
                           'Oswald Efficiency',
                           'prop_eff',
                           'thermal_eff',
                           'c_L',
                           'c_D',
                           'c_Di',
                           'c_D0']]
    aircrafts = aircrafts.groupby(['Company','Name','Type','YOI'], as_index=False).agg('mean')
    aircrafts.to_excel(r'C:\Users\PRohr\Desktop\Masterarbeit\Python\test_env\Databank.xlsx', index=False)





