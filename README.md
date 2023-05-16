# Aircraft Performance Code Documentation
## Repository Structure
All the relevant code is in the test_env folder. 
### master.py 
This is the main file, which executes the modelling pipeline. The Output Folder for all Graphs and all constants can be specified here. 
As an output the Excel File Databank.xlsx will be produced.

* database_creation.overallefficiency : Uses US DOT Schedule T2 and Data from Lee et al. to calculate Overall Efficiency regarding MJ/ASK and creates the Databank
* database_creation.emissions.to_vs_cruise_sfc : Using different sources, engines where both T/O and Cruise TSFC is known are gathered and a calibration between T/O and Cruise fuel consumption is made. 
* database_creation.emissions.icaoemssions : Scales the T/O TSFC from the ICAO Emissions Databank to Cruise TSFC
* database_creation.aircraft_engine_configurations : [Aircraft Database](https://aircraft-database.com/) is used to gather all relevant aircraft and engine parameters, and aswell aircraft-engine combinations. The engines are then matched to the engine of the ICAO Emissions Databank to connect the Cruise TSFC to the aircraft. Finally all values are added to the Databank
* database_creation.emissions.engine_statistics : Calculates and Plots some Engine Statistics regarding Dry Weight, Bypass Ratio, Pressure Ratio...
* database_creation.structuralefficiency : Calculates Structural Efficiency in OEW/Pax Exit Limit and adds it to the Databank
* database_creation.seats : Based on Data from the US DOT, real seating capacities for aircraft are averaged and added to the Databank
* database_creation.seatloadfactor : SLF measured by the US DOT and the ICAO are gathered. 
* database_creation.aerodynamics.aerodynamicefficiency : Using the Breguet Range Equation and Data regarding the Weight and Range of Aircraft from Airport Planning Manuals the Aerodynamic Efficiency is calculated. To do so, the TSFC calculated before is used. The results are then added to the Databank. 
* database_creation.emissions.therm_prop_eff : This file splits the Engine Efficiency into Propulsive and Thermal Efficiency by calculating the Propulsive Efficiency, assuming that propulsive efficiency * thermal efficiency = engine efficiency. The values are then added to the Databank.   
* database_creation.aggregate_per_aircraft : The Databank contains now multiple entries for each aircraft, accounting for different engines, different OEW and MTOW series. This file groups all the data on Aircraft Level. 
* database_creation.index_decomposition : Decomposes the technical Efficiency improvements MJ/ASK into Structural, Aerodynamic, Engine and Residual Efficiency.  
* database_creation.index_decomposition_operational : Integrates the SLF to calculate MJ/RPK and decomposes the efficiency gains into Structural, Aerodynamic, Engine, Operational and Residual.

### Database Creation
The folder database_creation contains all the files executed by the master.py. Further, the folder rawdata contains all Input Data and in the 
folder "graphs", all created figures will be saved.
### Tools
The tools folder contains some additionally helpful files, such as plotting properties or dictionaries to match the aircraft names from different sources.

## Quickstart
### Setup Repository
1. Clone this repository
```bash
git clone https://github.com/rohrerph/Master_Thesis_Codes.git
```
2. Install all needed Packages
3. Head over to the test_env.master.py File and execute the simulation