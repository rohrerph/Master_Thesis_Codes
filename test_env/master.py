import warnings
import database_creation.update_overall_efficiency
import database_creation.emissions.icaoemssions
import database_creation.emissions.to_vs_cruise_sfc
import database_creation.aircraft_engine_params
import database_creation.emissions.to_vs_cruise_plots
import database_creation.oew_pax_test
import database_creation.seats
import database_creation.seatloadfactor
import database_creation.aerodynamics.l_over_d_test
import database_creation.emissions.therm_prop_eff
import database_creation.per_aircraft
warnings.filterwarnings("ignore")

# Parameters
savefig = True
flight_vel = 240  # m/s
air_density = 0.4135  # kg/m^3
gravity = 9.81

print(' --> [START]')
print(' --> [CREATE AIRCRAFT DATABASE]: Load Demand Data from the US DOT...')
database_creation.update_overall_efficiency.calculate(savefig)
print(' --> [CREATE AIRCRAFT DATABASE]: Calibrate Linear Fit for Take-Off vs Cruise TSFC...')
linear_fit = database_creation.emissions.to_vs_cruise_sfc.calibrate(savefig)
print(' --> [CREATE AIRCRAFT DATABASE]: Scale Take-Off TFSC from ICAO emissions Databank to Cruise TSFC ...')
database_creation.emissions.icaoemssions.calculate(linear_fit)
print(' --> [CREATE AIRCRAFT DATABASE]: Add all Aircraft-Engine combinations and its Parameters ...')
database_creation.aircraft_engine_params.calculate(air_density, flight_vel)
print(' --> [CREATE AIRCRAFT DATABASE]: Create Graphs for Engine Statistics ...')
database_creation.emissions.to_vs_cruise_plots.calculate(savefig)
print(' --> [CREATE AIRCRAFT DATABASE]: Calculate OEW per Exit Limit ...')
#database_creation.oew_pax_test.calculate(savefig)
print(' --> [CREATE AIRCRAFT DATABASE]: Add Seats per Aircraft from US DOT ...')
#database_creation.seats.calculate()
print(' --> [CREATE ANNUAL VALUES]: Calculate Seat Load Factor and Airborne Efficiency ...')
#database_creation.seatloadfactor.calculate()
print(' --> [CREATE AIRCRAFT DATABASE]: Calculate L/D Ratio from Breguet Range Equation...')
#database_creation.aerodynamics.l_over_d_test.calculate(savefig, air_density, flight_vel, gravity)
print(' --> [CREATE AIRCRAFT DATABASE]: Split Engine Efficiency into Thermal and Propulsive Efficiency...')
#database_creation.emissions.therm_prop_eff.calculate(savefig)
print(' --> [CREATE AIRCRAFT DATABASE]: Summarize Data per Aircraft Type')
#database_creation.per_aircraft.calculate()
print(' --> [FINISH]')
