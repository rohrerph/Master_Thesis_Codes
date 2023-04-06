import pandas as pd
def preprocessing(T2, AC_types, airlines, airplanes):
    T2 = T2.dropna(subset=['AVL_SEAT_MILES_320', 'REV_PAX_MILES_140', 'AIRCRAFT_FUELS_921'])
    T2 = T2.loc[T2['AIRCRAFT_FUELS_921'] > 0]
    T2 = T2.loc[T2['AVL_SEAT_MILES_320'] > 0]
    T2 = T2.loc[T2['REV_PAX_MILES_140'] > 0]
    #next line acts as a control , that RPM is smaller than ASM, which is correct for all lines!
    T2 = T2.loc[T2['REV_PAX_MILES_140'] <= T2['AVL_SEAT_MILES_320']]
    # this subgroup 3 contains all "Major Carriers"
    T2 = T2.loc[T2['CARRIER_GROUP'] == 3]
    # subgroup 1 for aircraft passenger configuration
    T2 = T2.loc[T2['AIRCRAFT_CONFIG'] == 1]
    # Use the 19 Airlines
    T2 = T2.loc[T2['UNIQUE_CARRIER_NAME'].isin(airlines)]
    T2 = pd.merge(T2, AC_types, left_on='AIRCRAFT_TYPE', right_on='Code')
    T2 = T2.loc[T2['Description'].isin(airplanes)]
    T2['GAL/ASM'] = T2['AIRCRAFT_FUELS_921'] / T2['AVL_SEAT_MILES_320']
    T2['GAL/RPM'] = T2['AIRCRAFT_FUELS_921'] / T2['REV_PAX_MILES_140']
    T2 = T2.loc[T2['HOURS_AIRBORNE_650'] <= T2['ACRFT_HRS_RAMPTORAMP_630']]
    T2['Airborne Eff.'] = T2['HOURS_AIRBORNE_650'] / T2['ACRFT_HRS_RAMPTORAMP_630']
    T2['SLF']= T2['REV_PAX_MILES_140']/T2['AVL_SEAT_MILES_320']
    return(T2)
