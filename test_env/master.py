import warnings
import database_creation.overallefficiency
import database_creation.emissions.icaoemssions
import database_creation.emissions.to_vs_cruise_sfc
import database_creation.aircraft_engine_configurations
import database_creation.emissions.engine_statistics
import database_creation.structuralefficiency
import database_creation.seats
import database_creation.seatloadfactor
import database_creation.aerodynamics.aerodynamicefficiency
import database_creation.emissions.therm_prop_eff
import database_creation.aggregate_per_aircraft
warnings.filterwarnings("ignore")

# Parameters
savefig = True
flight_vel = 240  # m/s
km = 1.609344  # miles
heatingvalue_gallon = 142.2  # 142.2 MJ per Gallon of kerosene
heatingvalue_kg = 43.1  # MJ/kg
air_density = 0.4135  # kg/m^3
gravity = 9.81  # m/s^2

print(' --> [START]')
print(' --> [CREATE AIRCRAFT DATABASE]: Load Demand Data from the US DOT...')
database_creation.overallefficiency.calculate(savefig, km, heatingvalue_gallon)
print(' --> [CREATE AIRCRAFT DATABASE]: Calibrate Linear Fit for Take-Off vs Cruise TSFC...')
linear_fit = database_creation.emissions.to_vs_cruise_sfc.calibrate(savefig)
print(' --> [CREATE AIRCRAFT DATABASE]: Scale Take-Off TFSC from ICAO emissions Databank to Cruise TSFC ...')
database_creation.emissions.icaoemssions.calculate(linear_fit)
print(' --> [CREATE AIRCRAFT DATABASE]: Add all Aircraft-Engine combinations and its Parameters ...')
database_creation.aircraft_engine_configurations.calculate(heatingvalue_kg, air_density, flight_vel, savefig)
print(' --> [CREATE AIRCRAFT DATABASE]: Create Graphs for Engine Statistics ...')
database_creation.emissions.engine_statistics.calculate(savefig)
print(' --> [CREATE AIRCRAFT DATABASE]: Calculate OEW per Exit Limit ...')
database_creation.structuralefficiency.calculate(savefig)
print(' --> [CREATE AIRCRAFT DATABASE]: Add Seats per Aircraft from US DOT ...')
database_creation.seats.calculate()
print(' --> [CREATE ANNUAL VALUES]: Calculate Seat Load Factor and Airborne Efficiency ...')
database_creation.seatloadfactor.calculate(savefig)
print(' --> [CREATE AIRCRAFT DATABASE]: Calculate L/D Ratio from Breguet Range Equation...')
database_creation.aerodynamics.aerodynamicefficiency.calculate(savefig, air_density, flight_vel, gravity)
print(' --> [CREATE AIRCRAFT DATABASE]: Split Engine Efficiency into Thermal and Propulsive Efficiency...')
database_creation.emissions.therm_prop_eff.calculate(savefig, flight_vel)
print(' --> [CREATE AIRCRAFT DATABASE]: Summarize Data per Aircraft Type')
database_creation.aggregate_per_aircraft.calculate()
print(' --> [FINISH]')