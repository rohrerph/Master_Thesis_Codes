import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def calculate(savefig, folder_path, temp):
    # Parameters
    T1 = temp  # Kelvin, Air Temperature in Altitude
    T3_NOx = 2000  # Max Temp in Kelvin regarding NOx emissions
    T3s = np.linspace(1000, 2600, 1600)
    gamma = 1.4  # Isentropic Coefficient
    R = 287  # Gas Constant
    eta_c = 0.9  # Compressor Efficiency
    eta_t = 0.9  # Turbine Efficiency
    cp = R * gamma / (gamma - 1)
    pressure_ratios = np.linspace(10, 100, 90)

    results = []
    for pressure_ratio in pressure_ratios:
        for T3 in T3s:
            T2_s = T1 * (pressure_ratio) ** ((gamma - 1) / gamma)
            T2 = (T2_s - T1) / eta_c + T1
            T4_s = T3 * (1 / pressure_ratio) ** ((gamma - 1) / gamma)
            T4 = T3 - (T3 - T4_s) * eta_t
            T4_NOx_s = T3_NOx * (1 / pressure_ratio) ** ((gamma - 1) / gamma)
            T4_NOx = T3_NOx - (T3_NOx - T4_NOx_s) * eta_t
            heat = cp * ((T3 - T4) - (T2 - T1))
            heat_NOx = cp * ((T3_NOx - T4_NOx) - (T2 - T1))
            work = cp * (T3 - T2)
            work_NOx = cp * (T3_NOx - T2)

            thermal_eff = heat / work
            thermal_eff_NOx = heat_NOx / work_NOx

            results.append({'Burner Exit Temperature': T3,'Pressure Ratio': pressure_ratio, 'Thermal Efficiency': thermal_eff, 'NOx Thermal Efficiency': thermal_eff_NOx})

    df = pd.DataFrame(results)

    # Reshape data for heatmap
    efficiency_heatmap = df.pivot('Burner Exit Temperature', 'Pressure Ratio', 'Thermal Efficiency')

    efficiency_heatmap = efficiency_heatmap.mask(efficiency_heatmap < 0.4)
    data = efficiency_heatmap
    data = data.T

    # Create a figure and axes
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)

    # Plot the array as a heatmap using imshow
    im = ax.imshow(data[::-1], cmap='coolwarm', aspect='auto')
    contours = plt.contour(data[::-1], colors='black', linestyles='dashed', levels=10)
    plt.clabel(contours, inline=True, fontsize=8)

    cbar = plt.colorbar(im, label='Thermal Efficiency')

    # Set x and y labels
    ax.set_ylabel('Pressure Ratio')
    ax.set_xlabel('Burner Exit Temperature')

    new_xticks = [0, 200, 400, 600, 800, 1000, 1200, 1400, 1600]
    new_xlabels = ['1000', '1200', '1400','1600','1800','2000', '2200', '2400', '2600']
    plt.xticks(new_xticks, new_xlabels)

    new_yticks = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]
    new_ylabels = ['100', '90', '80','70','60','50', '40', '30', '20', '10']
    plt.yticks(new_yticks, new_ylabels)
    ax.vlines(1000,0,90, color='black', label='Temp NOx Limit', linewidth=3)
    ax.vlines(1600,0,90, color='black', label='Stoichiometric Limit', linewidth=3)
    ax.text(1000, -3, 'Temp NOx Limit', horizontalalignment='center', verticalalignment='center',  weight='bold')
    ax.text(1600, -3, 'Stochiometric Limit', horizontalalignment='center', verticalalignment='center',  weight='bold')
    ax.set_title(r'With $\eta_{Compressor}$ and $\eta_{Turbine}$ = 0.9', loc='left')
    if savefig:
        plt.savefig(folder_path + '/thermal_efficiency_limitation.png')
