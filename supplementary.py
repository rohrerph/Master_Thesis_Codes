# here i will create the list used in the dictionary
import dict
import pandas as pd

#Most common airlines
T52 = pd.read_csv(r"C:\Users\PRohr\Desktop\Masterarbeit\Data\T_SCHEDULE_T2.csv")
T52 = T52.dropna(subset = ['AVL_SEAT_MILES_320','REV_PAX_MILES_140','AIRCRAFT_FUELS_921'])

T52 = T52.loc[T52['CARRIER_GROUP'] == 3] #this subgroup 3 contains all "Major Carriers"
T52 = T52.loc[T52['AIRCRAFT_CONFIG'] == 1] #subgroup 1 for aircraft passenger configuration
most_common_airlines = T52['UNIQUE_CARRIER_NAME'].value_counts().head(20)



#What are the most common used aircraft types of these 20 airlines ?
airlines = dict.USAirlines().get_airlines()
T52 = T52.loc[T52['UNIQUE_CARRIER_NAME'].isin(airlines)]

aircraft_codes = pd.read_csv(r"C:\Users\PRohr\Desktop\Masterarbeit\Data\L_AIRCRAFT_TYPE (1).csv")

most_common_aircrafts = pd.merge(T52, aircraft_codes, left_on='AIRCRAFT_TYPE', right_on='Code')
most_common_aircrafts = most_common_aircrafts.drop(['Code', 'AIRCRAFT_TYPE'], axis = 1)

most_common_aircrafts = most_common_aircrafts['Description'].value_counts().head(20)

