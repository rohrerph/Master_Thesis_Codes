#%%
# runs code as interactive cell
# https://code.visualstudio.com/docs/python/jupyter-support-py

# IMPORTS #######################################

# plotting
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from matplotlib.ticker import FuncFormatter
cm = 1/2.54 # for inches-cm conversion

# data science
import numpy as np
import pandas as pd

# i/o
from pathlib import PurePath, Path

# SETUP #########################################

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.sans-serif": "Computer Modern",
    'font.size': 8
})

# DATA IMPORT ###################################

df_eff = pd.read_excel(
    io = 'data/data_aviation_radiative_forcing.xlsx',
    sheet_name = 'efficiency',
    header = 0,
    engine = 'openpyxl'
)

df_km = pd.read_csv(
    filepath_or_buffer = 'data/data_airline_capacity_and_traffic.csv',
    sep = ',',
    header = 'infer',
    index_col = False
)

# DATA MANIPULATION #############################

# FIGURE ########################################

# SETUP ######################

fig, ax = plt.subplots(
        num = 'main',
        nrows = 1,
        ncols = 1,
        dpi = 300,
        figsize=(16.5*cm, 5*cm), # A4=(210x297)mm
    )

ax2=ax.twinx()

# DATA #######################

x_eff = df_eff['year']
x_km = df_km['Year']
y_eff = df_eff['kg CO2/RPK']
y_km = df_km['Available seat kilometers; ASKs']

# AXIS LIMITS ################

#plt.ylim(0,150)

# TICKS AND LABELS ###########

ax.minorticks_on()
ax.tick_params(axis='x', which='minor', bottom=False)

def human_format(num, pos):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    return '%.0f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])

formatter = FuncFormatter(human_format)
ax2.yaxis.set_major_formatter(formatter)

# GRIDS ######################

ax.grid(which='major', axis='y', linestyle='-', linewidth = 0.5)
ax.grid(which='minor', axis='y', linestyle='--', linewidth = 0.5)

# AXIS LABELS ################

plt.xlabel("Year")
ax.set_ylabel("Carbon Intensity \n [kg CO$_2$/RPK]")
ax2.set_ylabel("RPK")

# PLOTTING ###################


ax.plot(
    x_eff,
    y_eff,
    color = 'black',
    linewidth = 1,
    label = 'Carbon Intensity'
)

ax2.plot(
    x_km,
    y_km,
    color = 'black',
    linewidth = 1,
    linestyle = 'dashed',
    label = 'RPK'
)

# LEGEND ####################

fig.legend(
    bbox_to_anchor=(1,1), bbox_transform=ax.transAxes,
    loc = 'upper right',
    fontsize = 'small',
    markerscale = 1.0,
    frameon = True,
    fancybox = False
)

# EXPORT #########################################

figure_name: str = str(Path.cwd().stem + '.pdf')

plt.savefig(
    fname = figure_name,
    format="pdf",
    bbox_inches='tight',
    transparent = False
)
# %%